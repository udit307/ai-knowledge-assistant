from pathlib import Path
import json
from utils import clean_text, chunk_text
from pypdf import PdfReader
from docx import Document
import pandas as pd

RAW_DATA_PATH = Path("data/raw")
OUTPUT_PATH = Path("data/processed/chunks.json")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100




def process_markdown_file(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    cleaned = clean_text(text)

    return cleaned

def process_txt_file(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    cleaned = clean_text(text)

    return cleaned

def process_pdf_file(file_path):

    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return clean_text(text)

def process_docx_file(file_path):

    doc = Document(file_path)

    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

    return clean_text(text)

def process_xlsx_file(file_path):

    df = pd.read_excel(file_path)

    text = df.to_string(index=False)

    return clean_text(text)

def process_csv_file(file_path):

    df = pd.read_csv(file_path)

    text = df.to_string(index=False)

    return clean_text(text)


def ingest_documents():

    all_chunks = []

    chunk_counter = 1

    markdown_files = list(RAW_DATA_PATH.glob("*.md"))
    txt_files = list(RAW_DATA_PATH.glob("*.txt"))
    pdf_files = list(RAW_DATA_PATH.glob("*.pdf"))
    docx_files = list(RAW_DATA_PATH.glob("*.docx"))
    csv_files = list(RAW_DATA_PATH.glob("*.csv"))


    print(f"Found {len(markdown_files)} markdown files")
    print(f"Found {len(txt_files)} text files")
    print(f"Found {len(pdf_files)} PDF files")
    print(f"Found {len(docx_files)} DOCX files")
    print(f"Found {len(csv_files)} CSV files")

    all_files = markdown_files + txt_files + pdf_files + docx_files + csv_files

    for file_path in all_files:

        print(f"Processing: {file_path.name}")

        if file_path.suffix == ".md":
            text = process_markdown_file(file_path)
        elif file_path.suffix == ".txt":
            text = process_txt_file(file_path)
        elif file_path.suffix == ".pdf":
            text = process_pdf_file(file_path)
        elif file_path.suffix == ".docx":
            text = process_docx_file(file_path)
        elif file_path.suffix == ".csv":
            text = process_csv_file(file_path)

        chunks = chunk_text(text)

        for chunk in chunks:

            chunk_data = {
                "chunk_id": f"chunk_{chunk_counter}",
                "source": file_path.name,
                "text": chunk,
               "metadata": {
                    "file_type": file_path.suffix,
                    "source_path": str(file_path),
                    "source_name": file_path.name,
                    "chunk_size": len(chunk)
}
            }

            all_chunks.append(chunk_data)

            chunk_counter += 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"\nSaved {len(all_chunks)} chunks")
    print(f"Output file: {OUTPUT_PATH}")


if __name__ == "__main__":
    ingest_documents()