# 🤖 Round 1B: Persona-Driven Document Intelligence

This module is part of the Adobe Hackathon 2025 project. Round 1B focuses on **understanding multiple PDF documents** in a collection, analyzing their content **based on a given persona and job-to-be-done (JTBD)**, and generating a structured output that ranks and summarizes the most relevant sections across PDFs.

---

## 📌 Objectives

- 🔍 **Analyze multiple documents per collection**
- 🧠 **Understand and extract relevant sections** based on a given persona and JTBD
- 🗂️ **Rank and summarize** important content across all PDFs
- 📊 Output a structured, persona-specific JSON for downstream usage

---

## 📁 Folder Structure

round1B/
├── Collection_1/
│ ├── PDFs/
│ ├── challenge1b_input.json
│ └── challenge1b_output.json ← Output generated here
│
├── Collection_2/
│ └── ...
│
├── Collection_3/
│ └── ...
│
├── engine.py ← Core logic: extraction, ranking, summarization
├── utils.py ← Utility functions for section extraction, cleaning, etc.
├── run.py ← CLI runner to trigger processing
├── requirements.txt ← All Python dependencies
└── README.md ← You're reading this


---

## ⚙️ How It Works

1. **Input**: 
   - A `challenge1b_input.json` with:
     - Persona description
     - Job-to-be-done (JTBD)
     - List of PDF files

2. **Processing**:
   - PDFs are parsed using layout-aware tools
   - Sentences and sections are extracted with page context
   - A semantic similarity model (`SentenceTransformer`) ranks relevance to the persona and JTBD
   - Top matching content is returned in structured format

3. **Output**:
   - A `challenge1b_output.json` containing:
     - Ranked relevant sections
     - Their source file and page
     - Summarized text
     - Confidence scores (optional)

---

## 🚀 How to Run

### 1. Install dependencies

### Sample Command with Docker

docker build -t intelligent-pdf1 .
docker run --rm -v "${PWD}:/app" intelligent-pdf1 python run.py Collection_1
#### On Windows PowerShell, use:
docker run --rm -v ${PWD}:/app intelligent-pdf1 python run.py Collection_1

## 📥 Input Format (challenge1b_input.json)

{
  "persona": "Travel Planner",
  "job": "Plan a trip of 4 days for a group of 10 college friends.",
  "files": [
    "daywise_plan.pdf",
    "local_guides.pdf",
    "budget_info.pdf"
  ]
}

## 📤 Output Format (challenge1b_output.json)

{
  "results": [
    {
      "file": "daywise_plan.pdf",
      "page": 2,
      "text": "Day 2 includes a beach visit, local street food tour, and night flea market.",
      "rank": 1,
      "score": 0.92
    },
    ...
  ]
}


## 🧠 NLP Model
Uses SentenceTransformer (all-MiniLM-L6-v2) for semantic similarity between section text and the persona+job prompt

Ranks sections based on cosine similarity score

Returns top N relevant snippets with metadata

## 📚 Dependencies
text
Copy
Edit
pdfminer.six==20221105
langdetect
sentence-transformers==2.2.2
scikit-learn

## 💡 Tips
Tune TOP_K value inside engine.py to control number of results

Improve clean_text() and extract_section_candidates() for better domain-specific accuracy

Use actual font sizes and page layout features to boost precision

## 🧼 Clean Up
To remove the Docker image:
docker rmi intelligent-pdf1

## 📃 License
This project is submitted as part of Adobe Hackathon 2025 and is intended for non-commercial evaluation purposes only.


---

You can paste this directly into the GitHub `README.md` editor under your `round1B/` folder. Let me know if you'd like:

- Badges (build passing, Python version, etc.)
- A sample input/output folder
- Screenshot of a sample PDF + output visualization


