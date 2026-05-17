import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


CHUNKS_PATH = Path("data/processed/chunks.json")

# Chroma DB storage folder
CHROMA_DB_PATH = "data/chroma_db"

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def load_chunks():

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)



def create_embeddings(chunks):

    print("Loading embedding model...")

    model = SentenceTransformer(EMBEDDING_MODEL)

    print(f"Received {len(chunks)} chunks")

    # Create Chroma client
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    # Create collection
    collection = client.get_or_create_collection(
        name="knowledge_base"
    )

    # OPTIONAL: Clear old vectors
    try:
        existing_ids = collection.get()["ids"]

        if existing_ids:
            collection.delete(ids=existing_ids)

            print("Old embeddings cleared")

    except Exception as e:
        print("No old embeddings found")

    for chunk in chunks:

        chunk_id = chunk["id"]

        text = chunk["text"]

        metadata = chunk["metadata"]

        # Generate embedding
        embedding = model.encode(text).tolist()

        # Store in Chroma
        collection.add(
            ids=[chunk_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata]
        )

        print(f"Embedded: {chunk_id}")

    print("\nEmbeddings stored successfully!")


# def create_embeddings():

#     print("Loading embedding model...")

#     model = SentenceTransformer(EMBEDDING_MODEL)

#     print("Loading chunks...")

#     chunks = load_chunks()

#     print(f"Loaded {len(chunks)} chunks")

#     # Create Chroma client
#     client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

#     # Create collection
#     collection = client.get_or_create_collection(
#         name="knowledge_base"
#     )

#     for chunk in chunks:

#         chunk_id = chunk["chunk_id"]

#         text = chunk["text"]

#         metadata = chunk["metadata"]

#         # Generate embedding
#         embedding = model.encode(text).tolist()

#         # Store in Chroma
#         collection.add(
#             ids=[chunk_id],
#             embeddings=[embedding],
#             documents=[text],
#             metadatas=[metadata]
#         )

#         print(f"Embedded: {chunk_id}")

#     print("\nEmbeddings stored successfully!")


# if __name__ == "__main__":
#     create_embeddings()