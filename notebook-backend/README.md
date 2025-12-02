# LEXAN-TRADE-BOOK
# Notebook Backend (Flask)

## Setup
1. Create a virtualenv:
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows

2. Install:
   pip install -r requirements.txt

3. Configure (optional)
   Copy `.env` and edit. By default uses SQLite file `notebook.db`.

4. Initialize DB & Migrate:
   export FLASK_APP=run.py
   flask db init
   flask db migrate -m "initial"
   flask db upgrade

5. Run:
   python run.py

## API endpoints
- `POST /api/upload` (multipart) -> files[] and optional form field `date` (YYYY-MM-DD)
- `GET /api/folders` -> list folders
- `GET /api/folders/<YYYY-MM-DD>` -> folder details (images + notes)
- `PUT /api/folders/<YYYY-MM-DD>/notes` -> JSON `{ "notes_html": "<p>...</p>" }`
- `POST /api/folders/<YYYY-MM-DD>/notes/images` -> form file `file`
- `GET /api/images/<id>`
- `DELETE /api/images/<id>`
- `GET /uploads/<subpath>` -> serves uploaded files in dev
