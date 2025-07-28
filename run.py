# round1B/run.py
import sys
import os
import json
from engine import process_documents

def process_collection(collection_name):
    input_path = os.path.join(collection_name, "challenge1b_input.json")
    output_path = os.path.join(collection_name, "challenge1b_output.json")
    pdf_folder = os.path.join(collection_name, "PDFs")

    print(f"🔍 Running engine for: {collection_name}")
    print(f"📥 Input: {input_path}")
    print(f"📂 PDFs from: {pdf_folder}")

    if not os.path.exists(input_path):
        print(f"❌ Input file not found: {input_path}")
        return

    result = process_documents(input_path, pdf_folder)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Output written to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run.py <Collection_Folder|all>")
        sys.exit(1)

    arg = sys.argv[1]
    if arg.lower() == "all":
        for d in os.listdir("."):
            if d.startswith("Collection_") and os.path.isdir(d):
                process_collection(d)
    else:
        process_collection(arg)
