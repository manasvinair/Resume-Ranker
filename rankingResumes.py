import sqlite3
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#function to get resumes from database
def get_resume():
    conn=sqlite3.connect("resume.db")
    cursor=conn.cursor()
    cursor.execute("SELECT filename, text FROM resumes")
    resumes=cursor.fetchall()
    conn.close()
    return resumes

#function to actually rank resumes based on job description
def rankResume(job_desc):
    resumes=get_resume()
    if not resumes:
        print("NO RESUMES FOUND!!!")
        return
    resume_texts = [text for _, text in resumes]
    filenames = [filename for filename, _ in resumes]
    
    # add job description to list of documents
    totaltext=resume_texts+[job_desc]
    
    #convert text into TF-IDF vectors
    vectorizer=TfidfVectorizer(stop_words='english')
    tfidf_matrix=vectorizer.fit_transform(totaltext)
    
    #compute similarity between job description and each resume
    job_vector=tfidf_matrix[-1] #last entry is job description
    resume_vector=tfidf_matrix[:-1]
    
    similarities=cosine_similarity(resume_vector,job_vector).flatten()
    
    #creating a dataframe for sorting
    ranked_resumes=pd.DataFrame({"FileName":filenames,"Similarities":similarities})
    ranked_resumes=ranked_resumes.sort_values(by="Similarities",ascending=False)
    
    print(ranked_resumes)
    return ranked_resumes

#example
job_desc=""""
Looking for a Data Scientist with experience in Python, Machine Learning, and NLP.
Familiarity with data visualization and SQL is a plus.
"""
rankResume(job_desc)
