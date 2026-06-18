<template>
  <div class="scan-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>扫码识别</span>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>

      <div class="scan-area">
        <div id="qr-reader" style="width: 100%; max-width: 500px; margin: 0 auto"></div>
        <div id="qr-error" class="error-msg" v-if="errorMsg">{{ errorMsg }}</div>
      </div>

      <div class="scan-tips">
        <el-alert type="info" :closable="false" show-icon>
          <template #title>
            将设备二维码对准摄像头，识别后自动跳转
          </template>
        </el-alert>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Html5Qrcode } from 'html5-qrcode'

const router = useRouter()
const errorMsg = ref('')
let scanner: Html5Qrcode | null = null

const startScan = async () => {
  try {
    scanner = new Html5Qrcode('qr-reader')
    await scanner.start(
      { facingMode: 'environment' },
      { fps: 10, qrbox: { width: 250, height: 250 } },
      (decodedText: string) => {
        // 解析 asset_code 或 URL
        let assetCode: string | null = null
        const urlMatch = decodedText.match(/\/scan\/result\/([A-Za-z0-9]+)/)
        const tagMatch = decodedText.match(/^asset:([A-Za-z0-9]+)$/)
        if (urlMatch) {
          assetCode = urlMatch[1]
        } else if (tagMatch) {
          assetCode = tagMatch[1]
        }
        if (assetCode) {
          stopScan()
          router.push(`/scan/result/${assetCode}`)
        }
      },
      () => { /* ignore scan errors */ }
    )
  } catch (err: any) {
    errorMsg.value = '无法启动摄像头: ' + (err.message || err)
  }
}

const stopScan = () => {
  if (scanner) {
    scanner.stop().catch(() => {})
    scanner = null
  }
}

onMounted(() => {
  startScan()
})

onUnmounted(() => {
  stopScan()
})
</script>

<style scoped>
.scan-area {
  text-align: center;
  padding: 20px 0;
}

.error-msg {
  color: #f56c6c;
  margin-top: 12px;
}

.scan-tips {
  margin-top: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
