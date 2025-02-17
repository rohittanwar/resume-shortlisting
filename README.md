### Resume shortlisting app

This repository contains the code for a Resume shortlisting application.

This application contains a FastAPI server, which exposes two endpoints as below - 

1. POST /extract-criteria -> Extract Ranking Criteria from Job Description
This endpoint accepts a job description file (PDF or DOCX), extracts key ranking criteria, and returns a structured JSON response.

Input Payload Example (Multipart Form-Data):
```
{
  "file": "<uploaded_job_description.pdf>"
}
```

Output Payload Example:
```
{
  "criteria": [
    "Must have certification XYZ",
    "5+ years of experience in Python development",
    "Strong background in Machine Learning"
  ]
}
```

2. POST /score-resumes -> Score Resumes Against Extracted Criteria

This endpoint accepts ranking criteria and multiple resumes (PDF or DOCX), processes the resumes, scores them based on the given criteria, and returns an CSV sheet containing each candidate's score. 

Input Payload Example (Multipart Form-Data):
```
{
  "criteria": [
    "Must have certification XYZ",
    "5+ years of experience in Python development",
    "Strong background in Machine Learning"
  ],
  "files": [
    "<uploaded_resume_1.pdf>",
    "<uploaded_resume_2.docx>",
    "<uploaded_resume_3.pdf>"
  ]
}
```
Output Payload Example (CSV Sheet):

```
Candidate Name,Must have certification in data science,5+ years of experience in Python development,Strong background in Machine Learning,Total Score
Charles Mc Turland,0,6,7,13
John Doe,0,2,1,3
Cynthia Dwayne,2,7,4,13
```