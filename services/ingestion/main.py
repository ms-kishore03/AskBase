from shared.config import settings
from services.ingestion.parsing import extract_text_from_pdf
from services.ingestion.chunking import generate_chunks
from shared.database import save_vector
from google import genai
from google.genai import types
import time

def process_document_pipeline(file_path: str, tenant_id: str, document_id: str) -> None:
    """
    Processes a document through the ingestion pipeline.
    """
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    # step 1: extract raw text from file

    raw_text = extract_text_from_pdf(file_path)

    # step 2: generate chunks from raw text

    chunks = generate_chunks(raw_text)

    # step 3: generate embeddings for each chunk and save to database

    for chunk in chunks:
        embedding = client.models.embed_content(
            model="gemini-embedding-001",
            contents=[chunk],
            config=types.EmbedContentConfig(output_dimensionality=768)
        )

        embed_vector = embedding.embeddings[0].values
        save_vector(tenant_id, document_id, chunk, embed_vector)
        time.sleep(1) # to avoid hitting rate limits

if __name__ == "__main__":
    # Example usage
    file_path = "/home/kishore/Documents/Github/AskBase/resources/sample.pdf"
    tenant_id = "tenant_123"
    document_id = "document_456"
    process_document_pipeline(file_path, tenant_id, document_id)

    
