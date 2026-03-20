import re
from utils.job_data import JOB_DATA
import os


def _load_text(file_path):
    # Basic text loader: if it's a text file, read; otherwise return empty
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ''


def parse_resume(file_path):
    """
    Lightweight resume parser (MVP):
    - If the file is plain text, extract skills by keyword matching against JOB_DATA skill lists.
    - Otherwise return a small default set.
    Returns dict: { skills: [...], education: str, experience: str }
    """
    text = _load_text(file_path)

    # Build skill vocabulary from JOB_DATA
    vocab = set()
    for job in JOB_DATA:
        for s in job.get('skills', []):
            vocab.add(s.lower())

    found = set()
    if text:
        lower = text.lower()
        for token in vocab:
            # simple substring match
            if token in lower:
                found.add(token.title())

    if not found:
        # fallback to demo values
        found = {"Python", "Flask", "Machine Learning"}

    parsed_data = {
        "skills": sorted(list(found)),
        "education": "",
        "experience": ""
    }
    return parsed_data
