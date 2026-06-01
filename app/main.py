from fastapi import FastAPI
from app.routers import admin, auth, documents, qa, users, workspaces

app = FastAPI(
    title="DocAI API",
    description="AI-powered document Q&A backend with RAG pipeline",
    version="1.0.0"
)

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(qa.router)
app.include_router(users.router)
app.include_router(workspaces.router)






