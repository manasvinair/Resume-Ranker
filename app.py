from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
from extract import extract_pdf, extract_doc
from store_resume import storeResume
from rankResume import rankResume
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# Upload folder configuration
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload folder exists

# Database initialization (Users and Resumes tables)
def init_db():
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()
    
    # Create users table for authentication
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    
    # Create resumes table to store resumes per user
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        filename TEXT,
        text TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    conn.commit()
    conn.close()

init_db()  # Initialize database when the app starts

# Function to store uploaded resume into the database
def store_resume(user_id, filename, text):
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO resumes (user_id, filename, text) VALUES (?, ?, ?)", (user_id, filename, text))
    conn.commit()
    conn.close()

# Route for user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)
        
        conn = sqlite3.connect("resume.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already taken!"
        conn.close()
        return redirect(url_for("login"))
    return render_template("register.html")

# Route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = sqlite3.connect("resume.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return redirect(url_for("upload_resume"))
        return "Invalid username or password!"
    return render_template("login.html")

# Route for logout
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

# Resume upload and ranking functionality
@app.route("/", methods=["GET", "POST"])
def upload_resume():
    if "user_id" not in session:
        return redirect(url_for("login"))  # Redirect to login if not authenticated
    
    if request.method == "POST":
        job_desc = request.form["job_description"]
        user_id = session["user_id"]
        
        # Clear previous resumes of the user before new upload
        conn = sqlite3.connect("resume.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM resumes WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        for file in request.files.getlist("resumes"):  # Handle multiple resume uploads
            if file.filename == "":
                continue
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            
            if filename.endswith(".pdf"):
                text = extract_pdf(filepath)
            elif filename.endswith(".docx"):
                text = extract_doc(filepath)
            else:
                continue  # Skip unsupported file types
            
            store_resume(user_id, filename, text)
        
        ranked_resumes = rankResume(job_desc)
        ranked_resumes["Similarities"] = ranked_resumes["Similarities"].fillna(0) * 100  # Convert to percentage
        return render_template("results.html", resumes=ranked_resumes.to_dict(orient="records"))
    
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)


#http://127.0.0.1:5000/