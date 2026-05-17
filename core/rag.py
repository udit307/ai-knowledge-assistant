from ollama import chat

from core.retriever import search


MODEL_NAME = "qwen2.5:3b"


def build_context(results):

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    return context


def ask_question(question):

    # Step 1: Retrieve relevant chunks
    results = search(question)

    # Step 2: Build context
    context = build_context(results)

    # Step 3: Create prompt
    prompt = f"""
You are an internal AI Knowledge Assistant.

Answer ONLY using the provided context.

If the answer is not found in the context, say:
"I could not find that information in the knowledge base."

Provide a clear and concise answer.

Context:
{context}

Question:
{question}
"""

    # Step 4: Send to Ollama
    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    return answer, results


if __name__ == "__main__":

    while True:

        question = input("\nAsk a question: ")

        if question.lower() == "exit":
            break

        answer, results = ask_question(question)

        print("\nANSWER:\n")
        print(answer)

        print("\nCITATIONS:\n")

        for source in results["metadatas"][0]:

            print(source.get("source_path", "Unknown Source"))