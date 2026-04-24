<template>
  <el-dialog title="上传图片" v-model="visible" width="500px">
    <el-upload
      drag
      action="#"
      :auto-upload="false"
      :on-change="handleFileChange"
      :file-list="fileList"
      multiple
    >
      <div class="el-upload__text">拖拽文件到此处或 <em>点击上传</em></div>
    </el-upload>
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="uploadFiles" :loading="uploading">开始上传</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { uploadImage } from '../api'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue', 'success'])

const visible = ref(props.modelValue)
const fileList = ref([])
const uploading = ref(false)

watch(() => props.modelValue, (val) => visible.value = val)
watch(visible, (val) => emit('update:modelValue', val))

const handleFileChange = (file, list) => {
  fileList.value = list
}

const uploadFiles = async () => {
  if (!fileList.value.length) return
  uploading.value = true
  
  const formData = new FormData()
  fileList.value.forEach(f => formData.append('files', f.raw))

  try {
    await uploadImage(formData)
    ElMessage.success('上传成功')
    fileList.value = []
    visible.value = false
    emit('success')
  } catch (err) {
    ElMessage.error('上传失败: ' + (err.response?.data?.detail || '未知错误'))
  } finally {
    uploading.value = false
  }
}
</script>