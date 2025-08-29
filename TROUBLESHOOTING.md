# File Upload Troubleshooting Guide

## Common Issues and Solutions

### 1. Files Not Appearing in Frontend

**Problem**: Files are uploaded successfully but don't show up in the frontend interface.

**Possible Causes and Solutions**:

#### A. Directory Permissions
```bash
# Check if uploads directory exists and has proper permissions
ls -la uploads/
# If directory doesn't exist or has wrong permissions:
mkdir -p uploads
chmod 755 uploads
```

#### B. File Listing Logic
- Check if the `upload_page` function in `main.py` is correctly scanning the uploads directory
- Ensure the template is receiving the files list properly
- Verify the Jinja2 template syntax in `upload.html`

#### C. Browser Cache Issues
- Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)
- Clear browser cache
- Check browser developer console for JavaScript errors

#### D. Server Restart Required
- After uploading files, the page needs to be refreshed to show new files
- The current implementation reloads the page after upload

### 2. Upload Fails

**Problem**: File upload returns an error or fails completely.

**Possible Causes and Solutions**:

#### A. File Size Limits
```python
# Add file size validation in main.py
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Check file size (e.g., 10MB limit)
    if file.size > 10 * 1024 * 1024:  # 10MB
        return {"error": "File too large", "status": "error"}
    # ... rest of upload logic
```

#### B. File Type Restrictions
```python
# Add file type validation
ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.jpg', '.png', '.doc', '.docx'}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return {"error": "File type not allowed", "status": "error"}
    # ... rest of upload logic
```

#### C. Disk Space Issues
```bash
# Check available disk space
df -h
# Clean up if needed
rm -rf uploads/*
```

### 3. Frontend Not Loading

**Problem**: The web interface doesn't load or shows errors.

**Possible Causes and Solutions**:

#### A. Server Not Running
```bash
# Check if server is running
ps aux | grep python
# Start server if not running
source venv/bin/activate
python3 main.py
```

#### B. Port Already in Use
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill process if needed
kill -9 <PID>
# Or use different port
uvicorn main:app --host 0.0.0.0 --port 8001
```

#### C. Template Issues
- Check if `templates/upload.html` exists
- Verify Jinja2 syntax
- Check for missing static files

### 4. File Download/View Issues

**Problem**: Files can't be downloaded or viewed.

**Possible Causes and Solutions**:

#### A. File Not Found
- Check if file exists in uploads directory
- Verify filename matches exactly (case-sensitive)
- Check file permissions

#### B. MIME Type Issues
```python
# Add proper MIME type detection
import mimetypes

@app.get("/files/{filename}")
async def get_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return FileResponse(file_path, media_type=mime_type)
    return {"error": "File not found"}
```

### 5. Performance Issues

**Problem**: Uploads are slow or the interface is unresponsive.

**Possible Causes and Solutions**:

#### A. Large File Handling
```python
# Add streaming for large files
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Use chunked upload for large files
    chunk_size = 1024 * 1024  # 1MB chunks
    # ... implement chunked upload logic
```

#### B. Memory Issues
- Monitor server memory usage
- Consider using async file operations
- Implement file cleanup for old uploads

### 6. Security Issues

**Problem**: Security vulnerabilities in file upload system.

**Possible Causes and Solutions**:

#### A. File Type Validation
```python
# Implement strict file type validation
import magic  # pip install python-magic

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Read first few bytes to detect real file type
    content = await file.read(1024)
    file_type = magic.from_buffer(content, mime=True)
    
    # Check against allowed MIME types
    ALLOWED_MIME_TYPES = ['text/plain', 'image/jpeg', 'image/png', 'application/pdf']
    if file_type not in ALLOWED_MIME_TYPES:
        return {"error": "File type not allowed", "status": "error"}
    
    # Reset file pointer
    await file.seek(0)
    # ... continue with upload
```

#### B. Path Traversal Protection
```python
# Ensure uploaded files can't access other directories
import os

@app.get("/files/{filename}")
async def get_file(filename: str):
    # Sanitize filename
    safe_filename = os.path.basename(filename)
    file_path = UPLOAD_DIR / safe_filename
    
    # Ensure file is within uploads directory
    try:
        file_path.resolve().relative_to(UPLOAD_DIR.resolve())
    except ValueError:
        return {"error": "Invalid file path"}
    
    if file_path.exists():
        return FileResponse(file_path)
    return {"error": "File not found"}
```

## Debugging Steps

1. **Check Server Logs**: Look for error messages in the terminal where the server is running
2. **Browser Developer Tools**: Check Console and Network tabs for errors
3. **Test API Endpoints**: Use curl or Postman to test endpoints directly
4. **Verify File System**: Check if files are actually being saved
5. **Check Permissions**: Ensure proper file and directory permissions

## Testing Checklist

- [ ] Server starts without errors
- [ ] Web interface loads correctly
- [ ] File upload works
- [ ] Uploaded files appear in the list
- [ ] Files can be viewed/downloaded
- [ ] Files can be deleted
- [ ] Error handling works properly
- [ ] Large files are handled correctly
- [ ] Invalid files are rejected

## Getting Help

If you're still experiencing issues:

1. Check the server logs for specific error messages
2. Verify all dependencies are installed correctly
3. Test with a simple file first
4. Check if the issue is browser-specific
5. Try restarting the server
6. Verify the file system has sufficient space and permissions