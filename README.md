
# Ascend App Instructions

Current Functionality:
- React chat → FastAPI → Parse free-form text into structured fields
- Store in PostgreSQL
- Visualize on a dashboard
- Parsing backends:
  1) **OpenAI** (recommended if you have a key)
  2) **PyTorch tiny classifier** (set `USE_PYTORCH=1`) (This is how I am currently running on my end.)

Future Functionality (will release November 12th):
- Add user sign-in system.
- Implement gamified Daily Tasks and Streaks.
- Integrate chatbot with OpenAI.
- Improve the main website dashboard.
- Improve mood classification - fixing null edge cases



# 0) Prereqs
- Node 18+
- Python 3.10+
- Docker Desktop (for PostgreSQL)

# 1) Start PostgreSQL
```bash
docker compose up -d
```

# 2) Backend
```bash
cd ascend_app/backend
cp .env.example .env
# (Optional) put your OPENAI_API_KEY in .env
# (Optional) to use PyTorch path: set USE_PYTORCH=1 in .env

python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/init_db.py

# if init_db throws error to install remaining dependencies:
pip install fastapi "uvicorn[standard]" SQLAlchemy pydantic python-dotenv

### 
uvicorn app.main:app --reload
```
API: http://localhost:8000

# 3) Frontend

# open another terminal

```bash
cd ascend_code/frontend
npm install
npm run dev
```
Open http://localhost:5173

# 4) Current Usage
Type a message about something you did today.

The message will parse → save → appear on the chart & table.
