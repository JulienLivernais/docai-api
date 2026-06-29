DocAI API
----------
A backend service that allows users to upload PDF documents, organize them into workspaces,
and ask questions about them using AI semantic search and LLM responses.

FEATURES
----------
- Register and login with JWT authentication (access + refresh tokens)
- Secure password hashing with bcrypt
- OAuth2 password flow
- RBAC (user / admin)
- Create and manage workspaces
- Upload multiple PDF documents per workspace
- Automatic text extraction and chunking
- Semantic search using Pinecone vector database
- AI-powered question answering using OpenAI Key and LangChain RAG pipeline

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
* Docker

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
auth
- POST /auth/register
- POST /auth/login
- POST /auth/refresh

users
- GET /users/me
- PATCH /users/me
- DELETE /users/me

workspaces
- GET /workspaces
- POST /workspaces
- PATCH /workspaces/{id}
- DELETE /workspaces/{id}

documents
- POST /documents/{workspace_id}/upload
- GET /documents/{workspace_id}
- DELETE /documents/{document_id}

QA
- POST /qa/ask
- GET /qa/history

admin
- GET /admin/users
- GET /users/by-email
- GET /users/by-username
- GET /users/{user_id}
- DELETE /admin/users/{id}

ADMIN
----------
- Create admin account: python -m scripts.create_admin
- docker compose exec app python -m scripts.create_admin

SETUP IN LOCAL
----------
1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in the values
5. Create the PostgreSQL database
6. Run migrations: `alembic upgrade head`
7. Start the server: `uvicorn app.main:app --reload`
8. Open swagger API docs: `http://localhost:8000/docs`

SETUP WITH DOCKER
----------
1. Clone the repository: git clone https://github.com/JulienLivernais/docai-api
2. Navigate to the project: cd docai-api
3. Copy the environment file and fill in the values: cd .env.examples to .env
4. Build and start the containers: docker compose up --build
5. Run database migrations: docker compose exec app alembic upgrade head
6. Create the admin account: docker compose exec app python -m scripts.create_admin
7. Open API docs: http://localhost:8000/docs
8. Stop the containers when done: docker compose down
