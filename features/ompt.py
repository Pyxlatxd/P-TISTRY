# features/ompt.py

TITLE_PAGE_PROMPT = """
You are an APA formatting assistant. 
Given the following text from the first page of a student paper, 
extract and return a JSON object with keys:

  title
  name
  affiliation
  course
  instructor
  date

The input text may include extra lines or noise. 
Try to correctly identify the title, student name, affiliation, course name, instructor, and date.

Return ONLY valid JSON. Example:

{{ "title": "My Research Paper", "name": "John Doe", "affiliation": "University of XYZ", "course": "Psychology 101", "instructor": "Dr. Smith", "date": "September 14, 2025" }}

Input text:
{input_text}
"""
