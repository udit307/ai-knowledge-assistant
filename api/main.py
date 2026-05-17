from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import UploadFile, File
import json
from core.embed import create_embeddings
from core.rag import ask_question
import time
from fastapi import UploadFile, File
import fitz  # PyMuPDF
import io
from core.utils import chunk_text
from database import db
from database.db import SessionLocal
from database.models import Document


app = FastAPI(
    title="AI Knowledge Assistant",
    description="Local RAG-based AI assistant",
    version="1.0"
)


# Request body schema
class AskRequest(BaseModel):
    question: str


@app.get("/")
def home():

    return {
        "message": "AI Knowledge Assistant API is running"
    }

#----------------- Question Answering Endpoint ----------------     
@app.post("/ask")
def ask(request: AskRequest):

    question = request.question

    start_time = time.time()

    answer, results = ask_question(question)

    end_time = time.time()

    latency = round(end_time - start_time, 2)

    citations = []

    for source in results["metadatas"][0]:

        citations.append(
            source.get("source_name", "Unknown Source")
        )

    return {
        "question": question,
        "answer": answer,
        "citations": citations,
        "latency_seconds": latency
    }

#----------------- Upload Endpoint ----------------


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    content = await file.read()

    file_extension = file.filename.split(".")[-1].lower()

    text = ""

    # TXT / MD / CSV
    if file_extension in ["txt", "md", "csv"]:

        text = content.decode("utf-8")

    # PDF
    elif file_extension == "pdf":

        pdf = fitz.open(stream=content, filetype="pdf")

        for page in pdf:
            text += page.get_text()

    else:
        return {
            "message": "Unsupported file type"
        }

    db = SessionLocal()

    document = Document(
        title=file.filename,
        content=text,
        file_type=file_extension,
        source_name=file.filename
    )

    db.add(document)

    db.commit()

    db.close()

    return {
        "message": f"{file.filename} uploaded successfully"
    }

# @app.post("/upload")
# async def upload_document(file: UploadFile = File(...)):

#     content = await file.read()

#     text = content.decode("utf-8")

#     db = SessionLocal()

#     document = Document(
#         title=file.filename,
#         content=text,
#         file_type=file.filename.split(".")[-1],
#         source_name=file.filename
#     )
#     db.add(document)

#     db.commit()

#     db.close()

#     return {
#         "message": "Document uploaded successfully"
#     }


#-------------- Reindexing Endpoint ----------------
@app.post("/reindex")
def reindex_documents():

    db = SessionLocal()

    documents = db.query(Document).all()

    print("TOTAL DOCS:", len(documents))

    all_chunks = []

    chunk_counter = 1

    for doc in documents:

        print("DOC FOUND:", doc.source_name)

        print("CONTENT:", doc.content[:100])

        chunks = chunk_text(doc.content)

        print("CHUNKS CREATED:", len(chunks))

        for chunk in chunks:

            all_chunks.append({

                "id": f"chunk_{chunk_counter}",

                "text": chunk,

                "metadata": {
                    "source_name": doc.source_name,
                    "file_type": doc.file_type
                }
            })

            chunk_counter += 1

    print("TOTAL CHUNKS:", len(all_chunks))

    with open(
        "data/processed/chunks.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(all_chunks, f, indent=2)

    create_embeddings(all_chunks)

    db.close()

    return {
        "message": "Reindexing completed",
        "chunks_created": len(all_chunks)
    }



# @app.post("/reindex")
# def reindex_documents():

#     db = SessionLocal()

#     documents = db.query(Document).all()

#     all_chunks = []

#     chunk_counter = 1

#     for doc in documents:

#         chunks = chunk_text(doc.content)

#         for chunk in chunks:

#             all_chunks.append({

#                 "id": f"chunk_{chunk_counter}",

#                 "text": chunk,

#                 "metadata": {
#                     "source_name": doc.source_name,
#                     "file_type": doc.file_type
#                 }
#             })

#             chunk_counter += 1

#     # Save chunks.json
#     with open(
#         "data/processed/chunks.json",
#         "w",
#         encoding="utf-8"
#     ) as f:

#         json.dump(all_chunks, f, indent=2)

#     # Create embeddings
#     create_embeddings(all_chunks)

#     db.close()

#     return {
#         "message": "Reindexing completed",
#         "chunks_created": len(all_chunks)
#     }

# def reindex_documents():
#     db = SessionLocal()
#     documents = db.query(Document).all()
#     all_chunks = []
#     for doc in documents:
#         chunks = chunk_text(doc.content)
#         for i, chunk in enumerate(chunks):
#             all_chunks.append({
#                 "id": f"doc_{doc.id}_chunk_{i}",
#                 "text": chunk,
#                 "metadata": {
#                 "source_name": doc.source_name,
#                 "file_type": doc.file_type
#                 }
#     })
#     create_embeddings(all_chunks)
#     db.close()
#     return {
#         "message": "Reindexing completed"
#     }
