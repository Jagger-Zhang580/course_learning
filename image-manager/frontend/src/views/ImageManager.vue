<template>
  <div>
    <div style="margin-bottom: 20px; display: flex; justify-content: space-between;">
      <el-button type="primary" @click="showUpload = true">📤 上传图片</el-button>
    </div>

    <el-row :gutter="20">
      <el-col :span="6" v-for="img in images" :key="img.id" style="margin-bottom: 20px;">
        <el-card :body-style="{ padding: '0px' }">
          <el-image 
            :src="img.url" 
            fit="cover" 
            style="width: 100%; height: 200px;"
            @click="previewImage(img.url)"
          />
          <div style="padding: 14px;">
            <span style="font-size: 12px; color: #999;">{{ img.filename }}</span>
            <div style="margin-top: 10px;">
              <el-button type="danger" size="small" @click="handleDelete(img.id)">删除</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-pagination
      style="margin-top: 20px; justify-content: center;"
      background
      layout="prev, pager, next"
      :total="total"
      :page-size="limit"
      @current-change="fetchImages"
    />

    <UploadDialog v-model="showUpload" @success="fetchImages" />

    <el-dialog v-model="showPreview" width="80%">
      <el-image :src="previewUrl" fit="contain" style="width: 100%;" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getImages, deleteImage } from '../api'
import UploadDialog from '../components/UploadDialog.vue'

const images = ref([])
const total = ref(0)
const page = ref(1)
const limit = ref(12)

const showUpload = ref(false)
const showPreview = ref(false)
const previewUrl = ref('')

const fetchImages = async (p = 1) => {
  page.value = p
  try {
    const { data } = await getImages(page.value, limit.value)
    images.value = data.items
    total.value = data.total
  } catch (err) {
    ElMessage.error('获取图片列表失败')
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定删除该图片吗？', '警告', { type: 'warning' })
    await deleteImage(id)
    ElMessage.success('删除成功')
    fetchImages(page.value)
  } catch {}
}

const previewImage = (url) => {
  previewUrl.value = url
  showPreview.value = true
}

onMounted(() => fetchImages())
</script>