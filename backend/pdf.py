import fitz


def extract_pdf_text(pdf_location: str) -> str:
    """
    Extract all text from a PDF and return it as a single string.
    """
    doc = fitz.open(pdf_location)
    all_text = [page.get_text().strip().replace("\n", " ") for page in doc]
    all_text = " ".join(all_text)
    return all_text


def chunk_text(text: str, chunk_size: int = 600, chunk_overlap: int = 100) -> str:
    """
    Chunk text into overlapping chunks.

    chunk_size: Amount of characters in a text chunk.
    chunk_overlap: Amount of characters overlapping between chunks.
    """
    chunks = [
        text[i : i + chunk_size]
        for i in range(0, len(text), chunk_size - chunk_overlap)
    ]
    return chunks
