from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.workspaces import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse
from app.models.users import User
from app.models.workspaces import Workspace
import uuid


router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("/", response_model=list[WorkspaceResponse])
def get_workspaces(current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    return db.query(Workspace).filter(Workspace.user_id == current_user.id).all()


@router.post("/", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
def create_workspace(workspace: WorkspaceCreate,
                     current_user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    new_workspace = Workspace(
        **workspace.model_dump(),
        user_id=current_user.id,
        pinecone_namespace=str(uuid.uuid4())
    )
    db.add(new_workspace)
    db.commit()
    db.refresh(new_workspace)
    return new_workspace


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(workspace_id: int,
                  current_user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id,
                                           Workspace.user_id == current_user.id).first()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    return workspace


@router.patch("/{workspace_id}", response_model=WorkspaceResponse)
def update_workspace(workspace_id: int, updated: WorkspaceUpdate,
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id,
                                           Workspace.user_id == current_user.id).first()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    if updated.name is not None:
        workspace.name = updated.name
    db.commit()
    db.refresh(workspace)
    return workspace


@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workspace(workspace_id: int, current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id,
                                      Workspace.user_id == current_user.id).first()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    db.delete(workspace)
    db.commit()




