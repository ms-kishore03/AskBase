from langchain_text_splitters import RecursiveCharacterTextSplitter

def generate_chunks(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """
    Generates chunks of text from a given text.

    Args:
        text (str): The text to be chunked.
        chunk_size (int): The size of each chunk.
        chunk_overlap (int): The overlap between chunks.

    Returns:
        list[str]: A list of text chunks.

    """
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
    chunks = text_splitter.split_text(text)
    return chunks