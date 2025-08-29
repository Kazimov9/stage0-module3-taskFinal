from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
from pathlib import Path
import uuid

app = FastAPI(title="File Upload API")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    """Main page with upload form"""
    # Get list of uploaded files
    files = []
    if UPLOAD_DIR.exists():
        for file_path in UPLOAD_DIR.iterdir():
            if file_path.is_file():
                files.append({
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                    "path": str(file_path)
                })
    
    return templates.TemplateResponse(
        "upload.html", 
        {"request": request, "files": files}
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload"""
    try:
        # Generate unique filename to avoid conflicts
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"filename": file.filename, "saved_as": unique_filename, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

@app.get("/files/{filename}")
async def get_file(filename: str):
    """Serve uploaded files"""
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        return FileResponse(file_path)
    return {"error": "File not found"}

@app.delete("/files/{filename}")
async def delete_file(filename: str):
    """Delete uploaded file"""
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        file_path.unlink()
        return {"message": "File deleted successfully"}
    return {"error": "File not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)