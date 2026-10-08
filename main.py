from fastapi import FastAPI, Request, Form, Depends, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
import shutil
from uuid import uuid4

from config import settings
from models import Base, TranslationRequest, TranslationStatus
from services.translator import FakeTranslator
from services.email import FakeEmailProvider

# Database Setup
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Translator Web App")
templates = Jinja2Templates(directory="templates")

# Initialize Services
translator = FakeTranslator()
email_provider = FakeEmailProvider()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def process_translation_task(request_id: str):
    """Background task to handle the translation and email dispatch."""
    db = SessionLocal()
    try:
        trans_req = db.query(TranslationRequest).filter(TranslationRequest.id == request_id).first()
        if not trans_req:
            return

        # 1. Update status to PROCESSING
        trans_req.status = TranslationStatus.PROCESSING
        db.commit()

        # 2. Perform Translation
        if trans_req.file_path:
            # File translation
            translated_file_path = translator.translate_file(trans_req.file_path, trans_req.target_lang)
            # For the sake of the result page, we'll read the translated content
            with open(translated_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                translated_text = f.read()
            attachments = [translated_file_path]
        else:
            # Text translation
            translated_text = translator.translate(trans_req.source_text, trans_req.target_lang)
            attachments = []

        # 3. Send Email
        email_subject = f"Your translation to {trans_req.target_lang}"
        email_body = f"Original text/file processed.\n\nTranslation:\n{translated_text[:500]}..."
        email_provider.send_email(trans_req.email, email_subject, email_body, attachments=attachments)

        # 4. Update status to COMPLETED
        trans_req.translated_text = translated_text
        trans_req.status = TranslationStatus.COMPLETED
        db.commit()

    except Exception as e:
        print(f"Error processing translation {request_id}: {e}")
        trans_req = db.query(TranslationRequest).filter(TranslationRequest.id == request_id).first()
        if trans_req:
            trans_req.status = TranslationStatus.FAILED
            trans_req.error_log = str(e)
            db.commit()
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    template = templates.env.get_template("index.html")
    return HTMLResponse(content=template.render(request=request))

@app.post("/translate")
async def translate_text(
    background_tasks: BackgroundTasks,
    email: str = Form(...),
    target_lang: str = Form(...),
    text: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # 1. Handle input (File vs Text)
    source_text = ""
    file_path = None

    if file:
        # Save uploaded file
        file_id = str(uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Read content for the DB record only if it's a text file
        _, ext = os.path.splitext(file.filename)
        if ext.lower() == '.txt':
            with open(file_path, "rb") as f:
                source_text = f.read().decode('utf-8', errors='ignore')
        else:
            source_text = f"[Binary file uploaded: {file.filename}]"
    elif text:
        source_text = text
    else:
        raise HTTPException(status_code=400, detail="Either text or a file must be provided")

    # 2. Create persistent record as PENDING
    new_request = TranslationRequest(
        email=email,
        source_text=source_text,
        file_path=file_path,
        target_lang=target_lang,
        status=TranslationStatus.PENDING
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    # 3. Enqueue background task
    background_tasks.add_task(process_translation_task, new_request.id)

    # 4. Redirect to result page immediately
    return RedirectResponse(url=f"/result/{new_request.id}", status_code=303)

@app.get("/result/{request_id}", response_class=HTMLResponse)
async def get_result(request: Request, request_id: str, db: Session = Depends(get_db)):
    trans_req = db.query(TranslationRequest).filter(TranslationRequest.id == request_id).first()
    if not trans_req:
        raise HTTPException(status_code=404, detail="Translation request not found")

    template = templates.env.get_template("result.html")
    return HTMLResponse(content=template.render(
        request=request,
        source=trans_req.source_text,
        translation=trans_req.translated_text,
        status=trans_req.status.value,
        id=trans_req.id
    ))
