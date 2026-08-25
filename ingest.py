import os
import pymupdf

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.embeddings import create_embeddings
from src.qdrant_store import create_collection, insert_chunks


DOCUMENTS_FOLDER = "documents"


def extract_text_from_pdf(pdf_path):

    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        if text.strip():

            pages.append({
                "text": text,
                "page": page_number + 1
            })

    document.close()

    return pages


def create_chunks():

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    all_chunks = []

    for filename in os.listdir(DOCUMENTS_FOLDER):

        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(
            DOCUMENTS_FOLDER,
            filename
        )

        print(f"\nProcessing: {filename}")

        pages = extract_text_from_pdf(pdf_path)

        print(f"Pages found: {len(pages)}")

        for page in pages:

            chunks = splitter.split_text(
                page["text"]
            )

            for chunk in chunks:

                all_chunks.append({
                    "text": chunk,
                    "document": filename,
                    "page": page["page"]
                })

    return all_chunks


def main():

    print("Starting document ingestion...")

    chunks = create_chunks()

    print(f"\nTotal chunks created: {len(chunks)}")

    if not chunks:
        print("No chunks found.")
        return
    print("\nCreating embeddings...")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = create_embeddings(texts)

    print("Embeddings created.")
    print("\nConnecting to Qdrant...")

    create_collection()

    print("\nUploading data to Qdrant...")

    insert_chunks(
        chunks,
        embeddings
    )

    print("\nIngestion completed successfully!")


if __name__ == "__main__":
    main()