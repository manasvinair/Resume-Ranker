# Resume Screening Web App  

## Overview  
This web application allows users to upload multiple resumes and ranks them based on their relevance to a given job description. The ranking is done using TF-IDF (Term Frequency-Inverse Document Frequency), ensuring that resumes most relevant to the job posting appear at the top.  

## Features  
- Upload multiple resumes in PDF or DOCX format  
- Store resumes in a database for later retrieval  
- Extract text from resumes for analysis  
- Rank resumes based on job description relevance  
- User authentication to ensure resumes remain private  
- Clean and organized UI with a modern, dark theme  

## Technologies Used  
- Backend: Python, Flask, SQLite  
- Frontend: HTML, CSS  
- Styling: Custom CSS with a dark, professional design  
- Database: SQLite for storing resumes  
- File Handling: Secure handling of uploaded files  

## How It Works  
1. Users need to create an account to upload resumes securely  
2. Select and upload multiple resumes in supported formats  
3. Provide a job description for ranking  
4. The system processes resumes using TF-IDF and sorts them by relevance  
5. A table displays ranked resumes with relevance scores  

## Future Enhancements  
- Improve ranking algorithm by focusing on skills and projects  
- Add admin dashboard for better management  
- Allow download of ranked resumes  
- Deploy the application online for global access  

## Deployment  
The app will be deployed using Render or Railway, linked with GitHub for automatic updates.  

This project provides a basic but functional resume screening tool, with room for future improvements.
