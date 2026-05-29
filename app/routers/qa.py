from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.documents import DocumentResponse
from app.models.workspaces import Workspace
from app.models.users import User
from app.models.documents import Document
from app.services.documents import save_file_temporarily, load_document, delete_file
from app.services.embeddings import chunk_data, insert_or_fetch_embeddings
from app.core.config import settings

router = APIRouter(prefix="/qa", tags=["qa"])

