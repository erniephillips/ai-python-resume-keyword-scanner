import pdfminer.high_level
import re
import docx

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = pdfminer.high_level.extract_text(pdf_path)
    text = re.sub(r'\s+', ' ', text)  # remove extra whitespace/newlines
    return text.strip()

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    doc = docx.Document(docx_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    text = " ".join(fullText)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
