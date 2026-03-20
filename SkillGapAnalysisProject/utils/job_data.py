"""
Minimal in-repo job requirements dataset for demo and testing.
Each entry represents a company role with a list of required skills.
In production this should be replaced by a job-api ingestion pipeline.
"""
JOB_DATA = [
    {
        "company": "DataCorp",
        "role": "Data Scientist",
        "skills": ["Python", "Machine Learning", "Pandas", "SQL", "Statistics", "Data Visualization"]
    },
    {
        "company": "WebWorks",
        "role": "Backend Developer",
        "skills": ["Python", "Flask", "Django", "REST", "SQL", "Unit Testing"]
    },
    {
        "company": "CloudNine",
        "role": "ML Engineer",
        "skills": ["Python", "Machine Learning", "Docker", "Kubernetes", "TensorFlow", "PyTorch"]
    },
    {
        "company": "FinAnalytics",
        "role": "Data Analyst",
        "skills": ["SQL", "Excel", "Power BI", "Data Visualization", "Python"]
    }
]
