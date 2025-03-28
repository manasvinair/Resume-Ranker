import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rankResume(job_desc):
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()
    cursor.execute("SELECT filename, text FROM resumes")
    resumes = cursor.fetchall()
    conn.close()

    if not resumes:
        return pd.DataFrame(columns=["Filename", "Similarities"])

    filenames = [r[0] for r in resumes]
    texts = [r[1] for r in resumes]

    # Compute TF-IDF similarity
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([job_desc] + texts)
    similarity_scores = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:]).flatten()

    # Create a DataFrame
    ranked_df = pd.DataFrame({"Filename": filenames, "Similarities": similarity_scores})
    ranked_df = ranked_df.sort_values(by="Similarities", ascending=False).reset_index(drop=True)
    
    return ranked_df
