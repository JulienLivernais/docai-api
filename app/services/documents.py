from langchain_community.document_loaders import PyPDFLoader
import os
import shutil
from fastapi import UploadFile
import logging

logger = logging.getLogger(__name__)


def load_document(file_path: str):
    name, extension = os.path.splitext(file_path)

    if extension == '.pdf':
        logger.info(f"Loading {file_path}")
        loader = PyPDFLoader(file_path)
    else:
        raise ValueError(f"Unsupported file format: {extension}")

    data = loader.load()
    return data


def save_file_temporarily(file: UploadFile) -> str:
    tmp_dir = "tmp"
    os.makedirs(tmp_dir, exist_ok=True)
    file_path = os.path.join(tmp_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


def delete_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)



