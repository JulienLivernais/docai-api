DOCUMENT INTELLIGENCE API - DocAI API (in progress)
----------
A backend service that allows users to upload PDF documents, organize them into workspaces,
and ask questions about them using AI semantic search and LLM responses.

FEATURES
----------
- Register and login with JWT authentication (access + refresh tokens)
- Secure password hashing with bcrypt
- OAuth2 password flow
- Role-based access control (user / admin)
- Create and manage workspaces
- Upload multiple PDF documents per workspace
- Automatic text extraction and chunking
- Semantic search using Pinecone vector database
- AI-powered question answering using OpenAI and LangChain RAG pipeline

STACK
----------
* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* JWT
* OAuth2
* LangChain
* Pinecone

DATABASE
----------
users
- id, username, email, hashed_password, is_admin, is_active, created_at

workspaces
- id, name, pinecone_namespace, user_id, created_at, updated_at

documents
- id, filename, file_path, content, workspace_id, created_at

qa_responses
- id, question, answer, workspace_id, created_at

API
----------
Auth
- POST /auth/register
- POST /auth/login
- POST /auth/refresh

Users
- GET /users/me
- PATCH /users/me
- DELETE /users/me

Workspaces
- GET /workspaces
- POST /workspaces
- PATCH /workspaces/{id}
- DELETE /workspaces/{id}

Documents
- POST /documents/upload
- GET /documents
- DELETE /documents/{id}

QA
- POST /qa/ask
- GET /qa/history

Admin
- GET /admin/users
- DELETE /admin/users/{id}

SETUP
----------
1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in the values
5. Create the PostgreSQL database
6. Run migrations: `alembic upgrade head`
7. Start the server: `uvicorn app.main:app --reload`
8. Open API docs: `http://localhost:8000/docs`

NOTES
----------
This API is a portfolio project demonstrating backend development with AI integration, including authentication,
vector search, and RAG pipeline.

