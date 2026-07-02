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

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/{workspace_id}", response_model=list[DocumentResponse])
def get_documents(workspace_id: int,
                  current_user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id,
                                           Workspace.user_id == current_user.id).first()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    return db.query(Document).filter(Document.workspace_id == workspace_id).all()


@router.post("/{workspace_id}/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_document(workspace_id: int,
                    file: UploadFile = File(...),
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):

    # workspace exists?
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.user_id == current_user.id
    ).first()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

    # upload documents, chunks, embeddings to vector database and delete pdf
    file_path = save_file_temporarily(file)
    data = load_document(file_path)
    chunks = chunk_data(data)
    insert_or_fetch_embeddings(settings.PINECONE_INDEX_NAME, chunks, workspace.pinecone_namespace)
    delete_file(file_path)

    # save document to DB
    new_document = Document(
        filename=file.filename,
        file_path=file_path,
        workspace_id=workspace_id
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    document = db.query(Document).join(Workspace).filter(Document.id == document_id,
                                                         Workspace.user_id == current_user.id).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    db.delete(document)
    db.commit()

