# LexHarmoni Backend

FastAPI backend for regulatory friction and inconsistency detection.

## Setup

1. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate Virtual Environment:**
   - **Windows:** `.\venv\Scripts\activate`
   - **Unix/macOS:** `source venv/bin/activate`

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the development server with hot-reload:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.
Documentation (Swagger UI) is at `http://localhost:8000/docs`.
