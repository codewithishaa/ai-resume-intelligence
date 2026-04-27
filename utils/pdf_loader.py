from langchain_community.document_loaders import PyPDFLoader
import re


def load_pdf_text(file_path: str) -> str:
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text = " ".join(doc.page_content for doc in documents)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()

    return text