from fastapi import FastAPI
from pydantic import BaseModel

from core.rag import ask_question
import time


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