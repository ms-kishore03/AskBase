from pypdf import PdfReader
from docx import Document

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file_path (str): The path to the PDF file.
    
    Returns:
        str: The extracted text from the PDF.
    """

    reader = PdfReader(file_path)
    text=[page.extract_text() for page in reader.pages if page.extract_text() is not None]
    
    result = " ".join(text)
    return result

def extract_text_from_docx(file_path: str) -> str:
    """
    Extracts text from a DOCX file.

    Args:
        file_path (str): The path to the DOCX file.
    
    Returns:
        str: The extracted text from the DOCX file.
    """

    document = Document(file_path)
    text = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]

    result = " ".join(text)

    return result