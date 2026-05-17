import re

def clean_text(text):
    """
    Clean unwanted spaces and symbols
    """

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split text into overlapping chunks
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

