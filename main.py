from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from analyzer import analyze_code
from auto_refactor import auto_refactor_code
from score import calculate_score, check_modularity
import os
import PyPDF2

# Initialize FastAPI
app = FastAPI(title="CodeRefine Pro")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_FOLDER = "../uploads"
ALLOWED_EXTENSIONS = {"py", "pdf"}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/")
def home():
    return {"message": "CodeRefine backend is running"}

# Analyze endpoint
@app.post("/analyze")
async def analyze(code: str = Form(None), file: UploadFile = File(None)):
    code_text = ""

    # Handle file upload
    if file:
        filename = file.filename
        if allowed_file(filename):
            contents = await file.read()
            if filename.endswith(".py"):
                code_text = contents.decode("utf-8")
            elif filename.endswith(".pdf"):
                reader = PyPDF2.PdfReader(contents)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        code_text += page_text + "\n"

    # Handle pasted code
    if code:
        code_text = code

    # No code provided
    if not code_text.strip():
        return JSONResponse({
            "score": 0,
            "issues": ["No code provided."],
            "refactored_code": ""
        })

    # Analyze style issues
    actual_issues = analyze_code(code_text)

    # Check for warnings (modularity)
    warnings = check_modularity(code_text)

    # Combine issues for display
    issues = actual_issues + warnings

    # Auto-refactor code
    refined_code = auto_refactor_code(code_text)

    # Calculate score (100 for perfect code)
    score = calculate_score(actual_issues)

    return JSONResponse({
        "score": score,
        "issues": issues,
        "refactored_code": refined_code
    })
