from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.qa_responses import QACreate, QAResponse
from app.models.qa_responses import QAResponse as QAResponseModel
from app.models.workspaces import Workspace
from app.models.users import User
from app.services.rag import ask_and_get_answer
from app.services.embeddings import get_vector_store
from app.core.config import settings

router = APIRouter(prefix="/qa", tags=["qa"])


@router.post("/ask", response_model=QAResponse, status_code=status.HTTP_201_CREATED)
async def ask(question: QACreate,
              current_user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):

    # workspace exists?
    workspace = db.query(Workspace).filter(
        Workspace.id == question.workspace_id, Workspace.user_id == current_user.id).first()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

    # get the vector
    vector_store = get_vector_store(settings.PINECONE_INDEX_NAME, workspace.pinecone_namespace)

    # ask question, get answer
    answer = await ask_and_get_answer(vector_store, question.question)

    # save question + answer
    new_qa = QAResponseModel(
        question=question.question,
        answer=answer,
        workspace_id=question.workspace_id,
    )

    db.add(new_qa)
    db.commit()
    db.refresh(new_qa)

    # return question + answer
    return new_qa


@router.get("/history/{workspace_id}", response_model=list[QAResponse])
async def get_qa_history(workspace_id: int,
                         current_user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    pass


@router.delete("/history/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ask(workspace_id: int,
                     current_user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    pass



