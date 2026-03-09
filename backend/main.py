from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.extractor import extract_text_from_file
from utils.clause_analyzer import analyze_contract

app = FastAPI(title="LexScan API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_contract_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".docx", ".txt")):
        raise HTTPException(status_code=400, detail="Unsupported file format. Use PDF, DOCX, or TXT.")

    raw_text = await extract_text_from_file(file)

    if not raw_text or len(raw_text.strip()) < 50:
        raise HTTPException(status_code=422, detail="Could not extract meaningful text from the file.")

    result = await analyze_contract(raw_text)

    return {
        "filename": file.filename,
        "char_count": len(raw_text),
        "analysis": result
    }

@app.get("/health")
def health():
    return {"status": "ok"}
