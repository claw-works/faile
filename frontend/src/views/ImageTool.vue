<template>
  <div class="image-tool">
    <h2>图片处理</h2>

    <div class="upload-area" @dragover.prevent @drop.prevent="onDrop" @click="$refs.fileInput.click()">
      <input ref="fileInput" type="file" accept="image/*" style="display:none" @change="onFileChange" />
      <span v-if="!originalUrl">拖拽或点击上传图片</span>
      <img v-else :src="originalUrl" class="preview-img" />
    </div>

    <div v-if="originalUrl" class="controls">
      <div class="control-group">
        <label>裁切模式</label>
        <button :class="{ active: cropMode }" @click="toggleCrop">{{ cropMode ? '✅ 裁切中' : '开启裁切' }}</button>
      </div>
      <div class="control-group">
        <label>宽度 (px)</label>
        <input v-model.number="width" type="number" placeholder="自动" />
      </div>
      <div class="control-group">
        <label>高度 (px)</label>
        <input v-model.number="height" type="number" placeholder="自动" />
      </div>
      <div class="control-group">
        <label>格式</label>
        <select v-model="format">
          <option value="webp">WebP</option>
          <option value="jpg">JPEG</option>
          <option value="png">PNG</option>
        </select>
      </div>
      <div class="control-group">
        <label>质量 {{ quality }}%</label>
        <input v-model.number="quality" type="range" min="10" max="100" />
      </div>
      <button class="btn-primary" @click="processImage" :disabled="loading">
        {{ loading ? '处理中...' : '处理图片' }}
      </button>
    </div>

    <div v-if="resultUrl" class="result">
      <h3>处理结果</h3>
      <img :src="resultUrl" class="preview-img" />
      <a :href="resultUrl" :download="`result.${format}`" class="btn-download">下载</a>
    </div>

    <!-- Cropper modal -->
    <div v-if="showCropper" class="cropper-modal">
      <div class="cropper-container">
        <img ref="cropImg" :src="originalUrl" />
        <div class="cropper-actions">
          <button @click="applyCrop" class="btn-primary">确认裁切</button>
          <button @click="showCropper = false">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.css'
import axios from 'axios'

export default {
  data() {
    return {
      file: null,
      originalUrl: null,
      resultUrl: null,
      width: null,
      height: null,
      format: 'webp',
      quality: 85,
      cropMode: false,
      showCropper: false,
      cropData: null,
      cropper: null,
      loading: false,
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
      this.originalUrl = URL.createObjectURL(f)
      this.resultUrl = null
      this.cropData = null
    },
    toggleCrop() {
      if (!this.cropMode) {
        this.showCropper = true
        this.cropMode = true
        this.$nextTick(() => {
          if (this.cropper) this.cropper.destroy()
          this.cropper = new Cropper(this.$refs.cropImg, { viewMode: 1 })
        })
      } else {
        this.cropMode = false
        this.cropData = null
        if (this.cropper) { this.cropper.destroy(); this.cropper = null }
        this.showCropper = false
      }
    },
    applyCrop() {
      if (this.cropper) {
        const d = this.cropper.getData(true)
        this.cropData = { x: d.x, y: d.y, w: d.width, h: d.height }
        this.cropper.destroy()
        this.cropper = null
      }
      this.showCropper = false
    },
    async processImage() {
      if (!this.file) return
      this.loading = true
      const form = new FormData()
      form.append('file', this.file)
      if (this.width) form.append('width', this.width)
      if (this.height) form.append('height', this.height)
      if (this.cropData) {
        form.append('crop_x', this.cropData.x)
        form.append('crop_y', this.cropData.y)
        form.append('crop_w', this.cropData.w)
        form.append('crop_h', this.cropData.h)
      }
      form.append('format', this.format)
      form.append('quality', this.quality)
      try {
        const res = await axios.post('/api/image/process', form, { responseType: 'blob' })
        this.resultUrl = URL.createObjectURL(res.data)
      } catch (e) {
        alert('处理失败: ' + (e.response?.data?.detail || e.message))
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.image-tool { padding: 20px 0; }
h2 { margin-bottom: 20px; }
.upload-area {
  border: 2px dashed #ccc; border-radius: 12px; padding: 40px;
  text-align: center; cursor: pointer; background: white; min-height: 200px;
  display: flex; align-items: center; justify-content: center;
}
.upload-area:hover { border-color: #4f46e5; }
.preview-img { max-width: 100%; max-height: 400px; border-radius: 8px; }
.controls { display: flex; flex-wrap: wrap; gap: 16px; margin: 20px 0; align-items: flex-end; background: white; padding: 20px; border-radius: 12px; }
.control-group { display: flex; flex-direction: column; gap: 4px; }
.control-group label { font-size: 12px; color: #666; }
.control-group input[type=number], .control-group select { padding: 6px 10px; border: 1px solid #ddd; border-radius: 6px; width: 120px; }
.control-group input[type=range] { width: 120px; }
.btn-primary { background: #4f46e5; color: white; border: none; padding: 8px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-primary.active { background: #16a34a; }
.result { margin-top: 20px; background: white; padding: 20px; border-radius: 12px; }
.result h3 { margin-bottom: 12px; }
.btn-download { display: inline-block; margin-top: 12px; background: #16a34a; color: white; padding: 8px 20px; border-radius: 8px; text-decoration: none; }
.cropper-modal { position: fixed; inset: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 100; }
.cropper-container { background: white; padding: 20px; border-radius: 12px; max-width: 90vw; max-height: 90vh; overflow: auto; }
.cropper-actions { display: flex; gap: 12px; margin-top: 12px; }
</style>
