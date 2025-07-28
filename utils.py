# round1B/utils.py
import re

def extract_section_candidates(text):
    lines = text.split("\n")
    sections = []
    current_title = None
    buffer = []

    for line in lines:
        line = line.strip()
        if re.match(r"^[A-Z][A-Za-z0-9\s\-:,]{3,60}$", line) and line == line.strip():
            if current_title and buffer:
                sections.append({
                    "title": current_title,
                    "content": " ".join(buffer)
                })
            current_title = line
            buffer = []
        else:
            if line:
                buffer.append(line)

    if current_title and buffer:
        sections.append({
            "title": current_title,
            "content": " ".join(buffer)
        })

    return sections

def clean_text(text):
    return re.sub(r"\s+", " ", text.strip())

