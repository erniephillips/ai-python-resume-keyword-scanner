import pdfminer.high_level
import re
import io
import docx

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file using a file-like object.
    Reads the entire content into bytes and wraps it with io.BytesIO.
    """
    pdf_bytes = pdf_file.read()
    pdf_io = io.BytesIO(pdf_bytes)
    text = pdfminer.high_level.extract_text(pdf_io)
    text = re.sub(r'\s+', ' ', text)  # remove extra whitespace/newlines
    return text.strip()

def extract_text_from_docx(docx_file):
    """Extracts text from a DOCX file using a file-like object.
    Reads the file content into bytes and wraps it in a BytesIO to ensure the stream is seekable.
    """
    docx_bytes = docx_file.read()
    docx_io = io.BytesIO(docx_bytes)
    doc = docx.Document(docx_io)
    fullText = [para.text for para in doc.paragraphs]
    text = " ".join(fullText)
    text = re.sub(r'\s+', ' ', text)  # remove extra whitespace/newlines
    return text.strip()
