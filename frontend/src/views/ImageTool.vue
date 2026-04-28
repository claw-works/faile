<template>
  <div class="image-tool">
    <h2>图片处理</h2>

    <div class="upload-area" @dragover.prevent @drop.prevent="onDrop" @click="!originalUrl && $refs.fileInput.click()">
      <input ref="fileInput" type="file" accept="image/*" style="display:none" @change="onFileChange" />

      <div v-if="!originalUrl" class="upload-placeholder">
        拖拽或点击上传图片
      </div>

      <div v-else class="image-wrapper" ref="imageWrapper">
        <img ref="cropImg" :src="originalUrl" class="preview-img" @load="onImageLoad" />
        <!-- 裁切遮罩：确认裁切后显示 -->
        <svg v-if="cropData && !cropMode" class="crop-overlay" :viewBox="`0 0 ${naturalW} ${naturalH}`" preserveAspectRatio="none">
          <defs>
            <mask id="cropMask">
              <rect width="100%" height="100%" fill="white" />
              <rect :x="cropData.x" :y="cropData.y" :width="cropData.w" :height="cropData.h" fill="black" />
            </mask>
          </defs>
          <rect width="100%" height="100%" fill="rgba(0,0,0,0.55)" mask="url(#cropMask)" />
          <rect :x="cropData.x" :y="cropData.y" :width="cropData.w" :height="cropData.h"
            fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="6 3" />
        </svg>
      </div>
    </div>

    <div v-if="originalUrl" class="toolbar">
      <button @click="$refs.fileInput.click()" class="btn-secondary">重新上传</button>

      <template v-if="!cropMode">
        <button @click="enableCrop" class="btn-secondary">✂️ 开启裁切</button>
      </template>
      <template v-else>
        <button @click="applyCrop" class="btn-primary">✅ 确认裁切</button>
        <button @click="cancelCrop" class="btn-secondary">取消</button>
      </template>

      <span v-if="cropData" class="crop-info">
        已裁切 {{ cropData.w }}×{{ cropData.h }} px
        <button @click="clearCrop" class="btn-link">清除</button>
      </span>
    </div>

    <div v-if="originalUrl" class="controls">
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
      <button class="btn-primary" @click="processImage" :disabled="loading || cropMode">
        {{ loading ? '处理中...' : '处理图片' }}
      </button>
    </div>

    <div v-if="resultUrl" class="result">
      <h3>处理结果</h3>
      <img :src="resultUrl" class="preview-img" />
      <a :href="resultUrl" :download="`result.${format}`" class="btn-download">⬇️ 下载</a>
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
      cropData: null,
      cropper: null,
      loading: false,
      naturalW: 1,
      naturalH: 1,
    }
  },
  beforeUnmount() {
    this.destroyCropper()
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
    onImageLoad(e) {
      this.naturalW = e.target.naturalWidth
      this.naturalH = e.target.naturalHeight
    },
    loadFile(f) {
      this.destroyCropper()
      this.cropMode = false
      this.cropData = null
      this.resultUrl = null
      this.file = f
      this.originalUrl = URL.createObjectURL(f)
    },
    enableCrop() {
      this.cropMode = true
      this.$nextTick(() => {
        this.cropper = new Cropper(this.$refs.cropImg, {
          viewMode: 1,
          autoCropArea: 0.8,
          movable: true,
          zoomable: false,
        })
      })
    },
    applyCrop() {
      if (this.cropper) {
        const d = this.cropper.getData(true)
        this.cropData = { x: d.x, y: d.y, w: d.width, h: d.height }
      }
      this.destroyCropper()
      this.cropMode = false
    },
    cancelCrop() {
      this.destroyCropper()
      this.cropMode = false
    },
    clearCrop() {
      this.cropData = null
    },
    destroyCropper() {
      if (this.cropper) {
        this.cropper.destroy()
        this.cropper = null
      }
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
  border: 2px dashed #ccc; border-radius: 12px;
  background: white; min-height: 200px;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}
.upload-area:hover { border-color: #4f46e5; }
.upload-placeholder { cursor: pointer; color: #999; font-size: 16px; padding: 60px; }
.image-wrapper { width: 100%; position: relative; }
.crop-overlay { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.preview-img { max-width: 100%; display: block; }

.toolbar {
  display: flex; align-items: center; gap: 10px;
  margin: 12px 0; flex-wrap: wrap;
}
.crop-info { font-size: 13px; color: #666; }
.btn-link { background: none; border: none; color: #4f46e5; cursor: pointer; font-size: 13px; padding: 0 4px; }

.controls {
  display: flex; flex-wrap: wrap; gap: 16px;
  align-items: flex-end; background: white;
  padding: 20px; border-radius: 12px; margin-bottom: 20px;
}
.control-group { display: flex; flex-direction: column; gap: 4px; }
.control-group label { font-size: 12px; color: #666; }
.control-group input[type=number], .control-group select {
  padding: 6px 10px; border: 1px solid #ddd; border-radius: 6px; width: 120px;
}
.control-group input[type=range] { width: 120px; }

.btn-primary {
  background: #4f46e5; color: white; border: none;
  padding: 8px 20px; border-radius: 8px; cursor: pointer; font-size: 14px;
}
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary {
  background: white; color: #333; border: 1px solid #ddd;
  padding: 8px 16px; border-radius: 8px; cursor: pointer; font-size: 14px;
}
.btn-secondary:hover { border-color: #4f46e5; color: #4f46e5; }

.result { background: white; padding: 20px; border-radius: 12px; }
.result h3 { margin-bottom: 12px; }
.btn-download {
  display: inline-block; margin-top: 12px;
  background: #16a34a; color: white;
  padding: 8px 20px; border-radius: 8px; text-decoration: none;
}
</style>
