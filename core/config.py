from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")