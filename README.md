# faile

> 谐音 file，文件处理小工具 🐾

图片裁切/缩放/格式转换 + PDF/Word 转 Markdown，专为 LLM 准备素材设计。

## 功能

- **图片处理**：拖拽上传，可视化裁切，缩放，输出 WebP / JPEG / PNG
- **文档转换**：PDF / Word (.docx) → Markdown + 提取图片

## 快速启动

```bash
docker compose up --build
```

- 前端：http://localhost:5173
- 后端 API：http://localhost:8000/docs

## 本地开发

**后端**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**前端**
```bash
cd frontend
npm install
npm run dev
```

## 项目结构

```
faile/
├── backend/
│   ├── main.py          # FastAPI 入口
│   ├── routers/         # image / doc 路由
│   ├── core/            # 处理逻辑
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── views/       # ImageTool / DocTool
│   │   └── App.vue
│   └── package.json
└── docker-compose.yml
```
