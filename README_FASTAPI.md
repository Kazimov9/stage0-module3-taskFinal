# FastAPI File Upload System

A complete file upload system built with FastAPI that includes:
- File upload functionality
- File listing and management
- Modern web interface
- File viewing and deletion capabilities

## Features

- ✅ Drag and drop file upload
- ✅ Real-time file listing
- ✅ File preview and download
- ✅ File deletion
- ✅ Modern, responsive UI
- ✅ Progress indicators
- ✅ Error handling

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the FastAPI server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

## API Endpoints

- `GET /` - Main page with upload form and file list
- `POST /upload` - Upload a file
- `GET /files/{filename}` - Download/view a file
- `DELETE /files/{filename}` - Delete a file

## Project Structure

```
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── templates/
│   └── upload.html     # Main HTML template
├── static/
│   └── style.css       # Additional CSS styles
├── uploads/            # Directory where files are stored
└── README_FASTAPI.md   # This file
```

## How it Works

1. **File Upload**: Files are uploaded via a form and stored in the `uploads/` directory with unique filenames
2. **File Listing**: The main page scans the uploads directory and displays all files
3. **File Management**: Users can view and delete files through the web interface
4. **File Serving**: Files are served directly by FastAPI for viewing/downloading

## Troubleshooting

### Files not appearing in frontend?

1. **Check the uploads directory**: Make sure the `uploads/` directory exists and has proper permissions
2. **Check file permissions**: Ensure the application has read/write permissions to the uploads directory
3. **Check browser console**: Look for any JavaScript errors in the browser developer tools
4. **Check server logs**: Look for any error messages in the FastAPI server output

### Common Issues:

1. **CORS issues**: If accessing from a different domain, you may need to add CORS middleware
2. **File size limits**: Large files may be rejected by default limits
3. **File type restrictions**: Check if there are any file type restrictions in your configuration

## Customization

- **File size limits**: Modify the upload endpoint to add size restrictions
- **File type restrictions**: Add validation for specific file types
- **Storage location**: Change the `UPLOAD_DIR` variable to store files elsewhere
- **UI customization**: Modify the HTML template and CSS for different styling

## Security Considerations

- Files are stored with unique names to prevent conflicts
- Consider adding authentication for production use
- Implement file type validation for security
- Add file size limits to prevent abuse
- Consider using cloud storage for production deployments