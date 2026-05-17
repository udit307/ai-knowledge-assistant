import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_DB_PATH = "data/chroma_db"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# Load model once
model = SentenceTransformer(EMBEDDING_MODEL)

# Load Chroma DB
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

collection = client.get_collection("knowledge_base")


def search(query, top_k=3):

    # Convert query into embedding
    query_embedding = model.encode(query).tolist()

    # Search Chroma
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    user_query = input("Enter your question: ")

    results = search(user_query)

    print("\nTop Results:\n")

    for i, doc in enumerate(results["documents"][0]):

        print(f"Result {i+1}")
        print(doc)
        print("-" * 50)