DocAI API
----------
A backend service that allows users to upload PDF documents, organize them into workspaces,
and ask questions about them using AI semantic search and LLM responses.

LIVE DEMO
----------
This API is deployed on Railway.
Swagger UI: https://docai-api-production-2a53.up.railway.app/docs

- Register your own account via POST /auth/register, then connect via POST /auth/login (use your email as username).
- Click "Try it out" to test.

Admin accounts are created via: python -m scripts.create_admin), 
not through the API (this is intentional, to keep admin creation restricted to the project owner).

WHY A CUSTOM RAG PIPELINE
----------
- Each user's documents are isolated in their own workspace (separate Pinecone namespace)
- Q&A history is saved and queryable, not lost like a chat session
- Everything is accessible via API, so it can plug into other apps
- Answers are based only on the uploaded documents, not general model knowledge

EXAMPLE
----------
Tested with a public domain article: 
- "The-French-Hood-Festival-collegium.pdf" (The French Hood – what it is and what it is not)

Sample responses from POST /qa/ask:

```json
{
  "question": "What is the French Hood?",
  "id": 20,
  "answer": "The French hood is a headdress that is commonly represented as a rigid item with a crescent-shaped protrusion on top, often decorated with jewels. It is sometimes referred to as \"chaperon à templette,\" which translates to a hood/hat with a headband. The French hood has its origins in France, specifically Brittany, and underwent various form changes during the late 15th and 16th centuries.",
  "workspace_id": 9,
  "created_at": "2026-07-02T01:37:40.312553Z"
}
```

```json
{
  "question": "What is the common color of the cap?",
  "id": 22,
  "answer": "The common colors of the cap are usually white, black, or red.",
  "workspace_id": 9,
  "created_at": "2026-07-02T01:39:51.299988Z"
}
```

```json
{
  "question": "What is the common representation of the French hood?",
  "id": 27,
  "answer": "The common representation of the French hood is that it is a rigid headdress with a crescent-shaped protrusion on top, often decorated with jewels.",
  "workspace_id": 9,
  "created_at": "2026-07-02T01:43:23.282742Z"
}
```

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
