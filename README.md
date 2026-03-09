# LexScan — AI Contract Intelligence
<img width="1466" height="802" alt="Screenshot 2026-03-09 at 6 12 26 PM" src="https://github.com/user-attachments/assets/b1e83c55-9edb-499b-83b2-61bea58da4cb" />


A professional legal contract analyser powered by Gemini AI. Upload any contract (PDF, DOCX, TXT) and get:

- **Risk Score** (0–100) with overall risk level
- **Dangerous Clauses** — exact excerpts with risk severity (CRITICAL / HIGH / MEDIUM)
- **Suggested Improvements** — before/after clause rewrites
- **Missing Clauses** — what should be added, with sample text
- **Positive Aspects** — what the contract does well
- **Negotiation Tips** — leverage points for your position

---

## Setup

### 1. Backend

```bash
cd backend
pip install -r requirements.txt

# Create your .env file
cp .env.example .env
# Edit .env and add your Gemini API key
```

Start the server:
```bash
uvicorn main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

### 2. Frontend

Open `frontend/index.html` directly in your browser — **no build step required**.

Or serve it with a simple HTTP server:
```bash
cd frontend
python -m http.server 5500
```

Then open `http://localhost:5500`

---

## Getting a Gemini API Key

1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Add it to `backend/.env`:
   ```
   GEMINI_API_KEY=your_key_here
   ```

---

## Project Structure

```
legal-analyzer/
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   └── utils/
│       ├── extractor.py        # PDF / DOCX / TXT text extraction
│       └── clause_analyzer.py  # Single structured Gemini API call
└── frontend/
    └── index.html              # Complete UI — no framework needed
```



---


> ⚠️ **Disclaimer:** LexScan is for informational purposes only and does not constitute legal advice. Always consult a qualified legal professional before signing any contract.
