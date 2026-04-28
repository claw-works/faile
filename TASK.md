# faile - File Processing Tool

Build a complete project with this structure:

```
faile/
├── backend/          # FastAPI Python backend
│   ├── main.py       # FastAPI app entry point
│   ├── routers/
│   │   ├── image.py  # Image processing endpoints
│   │   └── doc.py    # Document conversion endpoints
│   ├── core/
│   │   ├── image.py  # Pillow image processing logic
│   │   └── doc.py    # PDF/Word to markdown logic
│   └── requirements.txt
├── frontend/         # Vue 3 frontend
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── views/
│   │   │   ├── ImageTool.vue   # Image crop/resize/convert UI
│   │   │   └── DocTool.vue     # Doc to markdown UI
│   │   └── components/
│   │       └── CropEditor.vue  # Interactive crop with cropperjs
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
└── README.md
```

## Backend Requirements

### Image API (`/api/image/`)
- `POST /api/image/process` - Upload image, returns processed image
  - params: width, height, crop (x,y,w,h), format (webp/jpg/png), quality
- `POST /api/image/info` - Get image metadata

### Doc API (`/api/doc/`)
- `POST /api/doc/convert` - Upload PDF or Word file
  - Returns: { markdown: "...", images: [{filename, base64}] }
  - PDF: use pymupdf (fitz) to extract text and images
  - Word (.docx): use python-docx to extract text and images
  - Convert to clean markdown with proper headings, lists, tables

### requirements.txt
```
fastapi
uvicorn[standard]
python-multipart
Pillow
pymupdf
python-docx
markdownify
```

### CORS: allow all origins (for dev)

## Frontend Requirements

### ImageTool.vue
- File upload (drag & drop)
- Show original image preview
- Crop tool using cropperjs (npm: cropperjs)
- Controls: width, height inputs, format selector (webp/jpg/png), quality slider
- "Process" button → POST to backend → download result
- Show before/after preview

### DocTool.vue  
- File upload (drag & drop), accept .pdf .docx
- Upload → show markdown preview (use marked.js for rendering)
- Show extracted images as thumbnails
- Download buttons: markdown file, zip of images

### Routing: vue-router
- / → ImageTool
- /doc → DocTool
- Nav tabs to switch

### package.json deps: vue@3, vue-router@4, cropperjs, marked, axios

## docker-compose.yml
```yaml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
  frontend:
    build: ./frontend
    ports: ["5173:5173"]
```

## README.md
Quick start instructions in Chinese and English.

When completely finished, run:
openclaw system event --text "Done: faile project scaffolded" --mode now
