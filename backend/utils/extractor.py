import pdfplumber
import docx2txt
from fastapi import UploadFile
import io


async def extract_text_from_file(file: UploadFile) -> str:
    content = await file.read()

    if file.filename.endswith(".pdf"):
        return extract_pdf_text(content)
    elif file.filename.endswith(".docx"):
        return extract_docx_text(content)
    elif file.filename.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")
    else:
        return ""


def extract_pdf_text(content: bytes) -> str:
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {str(e)}")
    return text.strip()


def extract_docx_text(content: bytes) -> str:
    try:
        return docx2txt.process(io.BytesIO(content)).strip()
    except Exception as e:
        raise ValueError(f"Failed to read DOCX: {str(e)}")
