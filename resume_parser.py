import pdfminer.high_level
import re
def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = pdfminer.high_level.extract_text(pdf_path)
    text = re.sub(r'\s+', ' ', text) # Remove extra spaces/newlines
    return text.strip()