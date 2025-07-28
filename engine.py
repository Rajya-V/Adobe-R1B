# round1B/engine.py
import os
import json
import datetime
from sentence_transformers import SentenceTransformer, util
from pdfminer.high_level import extract_text
from utils import extract_section_candidates, clean_text

def process_documents(input_json_path, pdf_folder):
    with open(input_json_path, encoding="utf-8") as f:
        data = json.load(f)

    persona = data["persona"]["role"]
    job = data["job_to_be_done"]["task"]
    query = f"{persona}: {job}"

    # Load locally cached model
    model_path = "model_cache/models--sentence-transformers--all-MiniLM-L6-v2"
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    query_embedding = model.encode(query, convert_to_tensor=True)

    extracted = []
    for doc in data["documents"]:
        file_path = os.path.join(pdf_folder, doc["filename"])
        try:
            text = extract_text(file_path)
            sections = extract_section_candidates(text)
            for s in sections:
                s["document"] = doc["filename"]
                s["page_number"] = 1  # pdfminer can't extract page numbers reliably
                extracted.append(s)
        except Exception as e:
            print(f"❌ Failed to process {doc['filename']}: {e}")

    if not extracted:
        return {
            "metadata": {
                "input_documents": [doc["filename"] for doc in data["documents"]],
                "persona": persona,
                "job_to_be_done": job,
                "processing_timestamp": datetime.datetime.now().isoformat()
            },
            "extracted_sections": [],
            "subsection_analysis": []
        }

    corpus = [f"{x['title']}\n{x['content']}" for x in extracted]
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
    similarities = util.cos_sim(query_embedding, corpus_embeddings)[0]

    top_k = min(5, len(extracted))
    scored = sorted(zip(extracted, similarities), key=lambda x: x[1], reverse=True)[:top_k]

    extracted_sections = []
    subsection_analysis = []

    for rank, (sec, score) in enumerate(scored, 1):
        extracted_sections.append({
            "document": sec["document"],
            "section_title": sec["title"],
            "importance_rank": rank,
            "page_number": sec["page_number"]
        })
        subsection_analysis.append({
            "document": sec["document"],
            "refined_text": clean_text(sec["content"]),
            "page_number": sec["page_number"]
        })

    return {
        "metadata": {
            "input_documents": [doc["filename"] for doc in data["documents"]],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.datetime.now().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }
