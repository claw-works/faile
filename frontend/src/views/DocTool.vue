<template>
  <div class="doc-tool">
    <h2>文档转 Markdown</h2>

    <div class="upload-area" @dragover.prevent @drop.prevent="onDrop" @click="$refs.fileInput.click()">
      <input ref="fileInput" type="file" accept=".pdf,.docx,.doc" style="display:none" @change="onFileChange" />
      <span v-if="!filename">拖拽或点击上传 PDF / Word 文档</span>
      <span v-else>📄 {{ filename }}</span>
    </div>

    <button v-if="filename" class="btn-primary" @click="convert" :disabled="loading" style="margin-top:16px">
      {{ loading ? '转换中...' : '开始转换' }}
    </button>

    <div v-if="result" class="result">
      <div class="result-tabs">
        <button :class="{ active: tab === 'preview' }" @click="tab = 'preview'">预览</button>
        <button :class="{ active: tab === 'raw' }" @click="tab = 'raw'">Markdown 源码</button>
        <button v-if="result.images.length" :class="{ active: tab === 'images' }" @click="tab = 'images'">
          图片 ({{ result.images.length }})
        </button>
      </div>

      <div v-if="tab === 'preview'" class="markdown-preview" v-html="renderedMarkdown"></div>

      <div v-if="tab === 'raw'" class="raw-code">
        <pre>{{ result.markdown }}</pre>
        <button class="btn-download" @click="downloadMarkdown">下载 .md</button>
      </div>

      <div v-if="tab === 'images'" class="images-grid">
        <div v-for="img in result.images" :key="img.filename" class="img-card">
          <img :src="`data:${img.mime};base64,${img.base64}`" />
          <a :href="`data:${img.mime};base64,${img.base64}`" :download="img.filename" class="btn-download-sm">
            {{ img.filename }}
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'
import axios from 'axios'

export default {
  data() {
    return {
      file: null,
      filename: null,
      result: null,
      loading: false,
      tab: 'preview',
    }
  },
  computed: {
    renderedMarkdown() {
      return this.result ? marked(this.result.markdown) : ''
    }
  },
  methods: {
    onDrop(e) {
      const f = e.dataTransfer.files[0]
      if (f) this.loadFile(f)
    },
    onFileChange(e) {
      const f = e.target.files[0]
      if (f) this.loadFile(f)
    },
    loadFile(f) {
      this.file = f
      this.filename = f.name
      this.result = null
    },
    async convert() {
      if (!this.file) return
      this.loading = true
      const form = new FormData()
      form.append('file', this.file)
      try {
        const res = await axios.post('/api/doc/convert', form)
        this.result = res.data
        this.tab = 'preview'
      } catch (e) {
        alert('转换失败: ' + (e.response?.data?.detail || e.message))
      } finally {
        this.loading = false
      }
    },
    downloadMarkdown() {
      const blob = new Blob([this.result.markdown], { type: 'text/markdown' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = this.filename.replace(/\.[^.]+$/, '.md')
      a.click()
    }
  }
}
</script>

<style scoped>
.doc-tool { padding: 20px 0; }
h2 { margin-bottom: 20px; }
.upload-area {
  border: 2px dashed #ccc; border-radius: 12px; padding: 60px;
  text-align: center; cursor: pointer; background: white; font-size: 16px;
}
.upload-area:hover { border-color: #4f46e5; }
.btn-primary { background: #4f46e5; color: white; border: none; padding: 10px 24px; border-radius: 8px; cursor: pointer; font-size: 14px; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.result { margin-top: 24px; background: white; border-radius: 12px; overflow: hidden; }
.result-tabs { display: flex; border-bottom: 1px solid #eee; }
.result-tabs button { padding: 12px 20px; border: none; background: none; cursor: pointer; color: #666; }
.result-tabs button.active { color: #4f46e5; border-bottom: 2px solid #4f46e5; font-weight: 600; }
.markdown-preview { padding: 24px; line-height: 1.7; }
.markdown-preview :deep(h1) { font-size: 1.8em; margin: 16px 0 8px; }
.markdown-preview :deep(h2) { font-size: 1.4em; margin: 14px 0 6px; }
.markdown-preview :deep(h3) { font-size: 1.2em; margin: 12px 0 4px; }
.markdown-preview :deep(p) { margin: 8px 0; }
.markdown-preview :deep(ul), .markdown-preview :deep(ol) { padding-left: 24px; margin: 8px 0; }
.markdown-preview :deep(table) { border-collapse: collapse; width: 100%; margin: 12px 0; }
.markdown-preview :deep(td), .markdown-preview :deep(th) { border: 1px solid #ddd; padding: 8px 12px; }
.raw-code { padding: 24px; }
.raw-code pre { background: #f8f8f8; padding: 16px; border-radius: 8px; overflow: auto; font-size: 13px; max-height: 500px; }
.btn-download { display: inline-block; margin-top: 12px; background: #16a34a; color: white; padding: 8px 20px; border-radius: 8px; text-decoration: none; border: none; cursor: pointer; }
.images-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; padding: 24px; }
.img-card { display: flex; flex-direction: column; gap: 8px; align-items: center; }
.img-card img { max-width: 100%; border-radius: 8px; border: 1px solid #eee; }
.btn-download-sm { font-size: 12px; color: #4f46e5; text-decoration: none; word-break: break-all; text-align: center; }
</style>
