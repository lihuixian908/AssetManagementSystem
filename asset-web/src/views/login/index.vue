<template>
  <div class="login-container">
    <!-- 科技线条 -->
    <div class="tech-lines">
      <span class="tl tl-h1"></span><span class="tl tl-h2"></span><span class="tl tl-h3"></span>
      <span class="tl tl-v1"></span><span class="tl tl-v2"></span>
      <span class="tl tl-d1"></span><span class="tl tl-d2"></span><span class="tl tl-d3"></span><span class="tl tl-d4"></span>
      <span class="tl tl-d5"></span><span class="tl tl-d6"></span><span class="tl tl-d7"></span><span class="tl tl-d8"></span>
    </div>

    <!-- 世界地图轮廓 + 数据流 -->
    <svg class="world-map-svg" viewBox="0 0 1000 500" xmlns="http://www.w3.org/2000/svg">
      <!-- 大陆轮廓 -->
      <path class="continent" d="M150,120 L180,100 L220,110 L240,130 L230,160 L200,180 L170,170 L140,150 Z" />
      <path class="continent" d="M280,140 L320,120 L360,130 L380,160 L370,200 L340,220 L300,210 L270,180 Z" />
      <path class="continent" d="M420,100 L480,80 L520,100 L540,140 L520,180 L480,200 L440,190 L410,160 L400,130 Z" />
      <path class="continent" d="M560,120 L600,100 L640,110 L660,140 L650,180 L620,200 L580,190 L550,160 Z" />
      <path class="continent" d="M700,140 L740,120 L780,130 L800,160 L790,200 L760,220 L720,210 L690,180 Z" />
      <path class="continent" d="M200,250 L240,230 L280,240 L300,270 L290,310 L260,330 L220,320 L190,290 Z" />
      <path class="continent" d="M450,260 L500,240 L540,250 L560,280 L550,320 L520,340 L480,330 L440,300 Z" />
      <path class="continent" d="M650,280 L690,260 L730,270 L750,300 L740,340 L710,360 L670,350 L640,320 Z" />

      <!-- 节点 -->
      <circle class="map-node" cx="180" cy="140" r="3" />
      <circle class="map-node" cx="320" cy="160" r="3" />
      <circle class="map-node" cx="460" cy="140" r="4" />
      <circle class="map-node" cx="600" cy="150" r="3" />
      <circle class="map-node" cx="740" cy="170" r="3" />
      <circle class="map-node" cx="240" cy="280" r="3" />
      <circle class="map-node" cx="500" cy="290" r="4" />
      <circle class="map-node" cx="690" cy="310" r="3" />

      <!-- 连接线 -->
      <line class="connection-line" x1="180" y1="140" x2="320" y2="160" />
      <line class="connection-line" x1="320" y1="160" x2="460" y2="140" />
      <line class="connection-line" x1="460" y1="140" x2="600" y2="150" />
      <line class="connection-line" x1="600" y1="150" x2="740" y2="170" />
      <line class="connection-line" x1="460" y1="140" x2="500" y2="290" />
      <line class="connection-line" x1="500" y1="290" x2="690" y2="310" />
      <line class="connection-line" x1="240" y1="280" x2="500" y2="290" />
      <line class="connection-line" x1="320" y1="160" x2="240" y2="280" />

      <!-- 数据流动点 -->
      <circle class="data-flow" cx="180" cy="140" r="2">
        <animateMotion dur="3s" repeatCount="indefinite" path="M180,140 L320,160 L460,140 L600,150 L740,170" />
      </circle>
      <circle class="data-flow" cx="460" cy="140" r="2">
        <animateMotion dur="4s" repeatCount="indefinite" path="M460,140 L500,290 L690,310" />
      </circle>
      <circle class="data-flow" cx="240" cy="280" r="2">
        <animateMotion dur="3.5s" repeatCount="indefinite" path="M240,280 L500,290 L690,310" />
      </circle>
    </svg>

    <!-- 浮动粒子 -->
    <div class="particles">
      <span class="particle p1"></span>
      <span class="particle p2"></span>
      <span class="particle p3"></span>
      <span class="particle p4"></span>
      <span class="particle p5"></span>
      <span class="particle p6"></span>
      <span class="particle p7"></span>
      <span class="particle p8"></span>
      <span class="particle p9"></span>
      <span class="particle p10"></span>
    </div>

    <div class="robot-section">
      <div class="float-tag tag-1">二维码管理</div>
      <div class="float-tag tag-2">资产追踪</div>
      <div class="float-tag tag-3">生命周期</div>
      <div class="float-tag tag-4">借还管理</div>
      <img
        src="/robot.png"
        alt="robot"
        class="robot-image"
      />
    </div>

    <div class="login-content">

      <div class="login-brand">
        <h1 class="brand-title">固定资产管理系统</h1>
        <p class="brand-subtitle">企业资产全生命周期管理平台</p>
        <p class="brand-tagline">资产登记 · 借还管理 · 二维码追踪 · 生命周期管理</p>
      </div>

      <el-card class="login-card">
        <div class="login-header">
          <h3 class="login-welcome">欢迎回来 👋</h3>
          <p class="login-hint">
            登录您的资产管理工作台
          </p>
        </div>

        <el-form
          :model="form"
          :rules="rules"
          ref="formRef"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="用户名"
              :prefix-icon="User"
              class="login-input"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="密码"
              :prefix-icon="Lock"
              show-password
              class="login-input"
            />
          </el-form-item>

          <el-form-item>
            <el-checkbox v-model="rememberMe">
              记住密码
            </el-checkbox>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              class="login-btn"
              :loading="loading"
              @click="handleLogin"
            >
              {{ loading ? '登录中...' : '登 录' }}
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { login } from '@/api/auth'
import { useUserStore } from '@/stores/user'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const rememberMe = ref(false)

const form = reactive({
  username: '',
  password: '',
})

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const handleLogin = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    const { data } = await login(form.username, form.password)
    userStore.setToken(data.data.access_token)
    ElMessage.success('登录成功')
    const redirect = localStorage.getItem('redirect')
    if (redirect) {
      localStorage.removeItem('redirect')
      router.push(redirect)
    } else {
      router.push('/')
    }
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ====== 科技网格背景 ====== */
.login-container {
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 80px;
  padding: 0 6%;
  overflow: hidden;
  background: linear-gradient(135deg, #0a1628 0%, #132244 40%, #1a3366 100%);
}

/* 网格线 */
.login-container::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(64, 158, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(64, 158, 255, 0.04) 1px, transparent 1px);
  background-size: 60px 60px;
  z-index: 0;
}

/* 光晕 */
.login-container::after {
  content: '';
  position: absolute;
  top: -30%;
  right: -10%;
  width: 700px;
  height: 700px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(64, 158, 255, 0.1), transparent 70%);
  z-index: 0;
}

/* ====== 科技线条 ====== */
.tech-lines {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.tl {
  position: absolute;
  display: block;
}

/* 水平线 */
.tl-h1 {
  top: 18%;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(64,158,255,.4) 20%, rgba(64,158,255,.4) 80%, transparent);
}

.tl-h2 {
  top: 62%;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(64,158,255,.3) 30%, rgba(64,158,255,.3) 70%, transparent);
}

.tl-h3 {
  bottom: 22%;
  right: 0;
  width: 50%;
  height: 1px;
  background: linear-gradient(90deg, rgba(64,158,255,.25), transparent);
}

/* 竖线 */
.tl-v1 {
  top: 0;
  right: 28%;
  width: 1px;
  height: 100%;
  background: linear-gradient(180deg, transparent, rgba(64,158,255,.25) 40%, rgba(64,158,255,.25) 60%, transparent);
}

.tl-v2 {
  top: 0;
  left: 18%;
  width: 1px;
  height: 100%;
  background: linear-gradient(180deg, transparent, rgba(64,158,255,.18) 35%, rgba(64,158,255,.18) 65%, transparent);
}

/* 光点 */
.tl-d1 { top: 20%; left: 15%; width: 6px; height: 6px; border-radius: 50%; background: rgba(64,158,255,.8); box-shadow: 0 0 16px rgba(64,158,255,.7); }
.tl-d2 { top: 65%; right: 22%; width: 5px; height: 5px; border-radius: 50%; background: rgba(64,158,255,.7); box-shadow: 0 0 14px rgba(64,158,255,.6); }
.tl-d3 { bottom: 30%; left: 35%; width: 5px; height: 5px; border-radius: 50%; background: rgba(64,158,255,.65); box-shadow: 0 0 12px rgba(64,158,255,.55); }
.tl-d4 { top: 40%; right: 15%; width: 7px; height: 7px; border-radius: 50%; background: rgba(64,158,255,.75); box-shadow: 0 0 18px rgba(64,158,255,.65); }
.tl-d5 { top: 12%; left: 55%; width: 5px; height: 5px; border-radius: 50%; background: rgba(64,158,255,.7); box-shadow: 0 0 14px rgba(64,158,255,.6); }
.tl-d6 { bottom: 18%; right: 40%; width: 6px; height: 6px; border-radius: 50%; background: rgba(64,158,255,.75); box-shadow: 0 0 16px rgba(64,158,255,.65); }
.tl-d7 { top: 50%; left: 8%; width: 4px; height: 4px; border-radius: 50%; background: rgba(64,158,255,.6); box-shadow: 0 0 10px rgba(64,158,255,.5); }
.tl-d8 { bottom: 45%; right: 8%; width: 5px; height: 5px; border-radius: 50%; background: rgba(64,158,255,.7); box-shadow: 0 0 14px rgba(64,158,255,.6); }

/* ====== 世界地图 + 数据流背景 ====== */
/* ====== 世界地图 + 数据流 ====== */
.world-map-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
  opacity: 0.25;
}

.continent {
  fill: none;
  stroke: rgba(64, 158, 255, 0.3);
  stroke-width: 1;
}

.map-node {
  fill: rgba(64, 158, 255, 0.9);
  filter: drop-shadow(0 0 4px rgba(64, 158, 255, 0.8));
}

.connection-line {
  stroke: rgba(64, 158, 255, 0.25);
  stroke-width: 1;
  stroke-dasharray: 4 4;
}

.data-flow {
  fill: rgba(64, 158, 255, 1);
  filter: drop-shadow(0 0 6px rgba(64, 158, 255, 0.9));
}

/* ====== 浮动粒子 ====== */
.particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: rgba(64, 158, 255, 0.8);
  box-shadow: 0 0 10px rgba(64, 158, 255, 0.6);
  animation: particleFloat 8s ease-in-out infinite;
}

.p1 { top: 10%; left: 10%; animation-delay: 0s; }
.p2 { top: 25%; left: 80%; animation-delay: 1s; }
.p3 { top: 40%; left: 20%; animation-delay: 2s; }
.p4 { top: 55%; left: 70%; animation-delay: 3s; }
.p5 { top: 70%; left: 30%; animation-delay: 4s; }
.p6 { top: 85%; left: 60%; animation-delay: 5s; }
.p7 { top: 15%; left: 50%; animation-delay: 6s; }
.p8 { top: 35%; left: 90%; animation-delay: 7s; }
.p9 { top: 60%; left: 5%; animation-delay: 1.5s; }
.p10 { top: 75%; left: 45%; animation-delay: 3.5s; }

@keyframes particleFloat {
  0%, 100% {
    transform: translateY(0) translateX(0);
    opacity: 0.8;
  }
  25% {
    transform: translateY(-20px) translateX(10px);
    opacity: 1;
  }
  50% {
    transform: translateY(-10px) translateX(-15px);
    opacity: 0.6;
  }
  75% {
    transform: translateY(-30px) translateX(5px);
    opacity: 0.9;
  }
}

/* ====== 机器人 ====== */
.robot-section {
  position: relative;
  flex: 0 0 auto;
  z-index: 1;
  margin-top: 60px;
  margin-right: 40px;
  animation: robotFloat 4s ease-in-out infinite;
}

.robot-section::after {
  content: '';
  position: absolute;
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
  width: 300px;
  height: 60px;
  border-radius: 50%;
  background: radial-gradient(ellipse, rgba(64,158,255,.2), transparent);
  filter: blur(10px);
}

/* 浮动标签 */
.float-tag {
  position: absolute;
  padding: 8px 20px;
  font-size: 15px;
  color: rgba(255,255,255,.8);
  background: rgba(59,130,246,.12);
  border: 1px solid rgba(59,130,246,.35);
  border-radius: 20px;
  white-space: nowrap;
  pointer-events: none;
  animation: tagFloat 4s ease-in-out infinite;
}

.tag-1 { top: 2%; left: -14%; z-index: 2; animation-delay: 0s; }
.tag-2 { top: 38%; left: -20%; z-index: 2; animation-delay: 1.2s; }
.tag-3 { bottom: 25%; left: -10%; z-index: 2; animation-delay: 2.4s; }
.tag-4 { top: 45%; right: -12%; z-index: 2; animation-delay: 0.8s; }

@keyframes tagFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

@keyframes robotFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12px); }
}

.robot-image {
  width: 520px;
  transform: scale(1.35);
  image-rendering: pixelated;
  filter:
    drop-shadow(0 40px 80px rgba(0, 0, 0, 0.4))
    drop-shadow(0 0 100px rgba(64, 158, 255, 0.18));
}

/* ====== 右侧内容 ====== */
.login-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 0 0 auto;
  margin-bottom: 80px;
  z-index: 2;
}

.login-brand {
  text-align: center;
  margin-bottom: 24px;
}

.brand-title {
  margin: 0;
  font-size: 58px;
  font-weight: 800;
  color: #fff;
  letter-spacing: 8px;
  text-align: center;
  text-shadow:
    0 0 60px rgba(64, 158, 255, 0.4),
    0 4px 8px rgba(0, 0, 0, 0.3);
  white-space: nowrap;
}

.brand-subtitle {
  margin-top: 14px;
  font-size: 20px;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: 4px;
  text-align: center;
}

.brand-tagline {
  margin-top: 14px;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.35);
  letter-spacing: 2px;
}

/* ====== 玻璃拟态卡片 ====== */
.login-card {
  width: 560px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow:
    0 25px 70px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

.login-card :deep(.el-card__body) {
  padding: 52px 48px;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-welcome {
  margin: 0;
  font-size: 32px;
  font-weight: 700;
  color: #fff;
}

.login-hint {
  margin-top: 10px;
  color: rgba(255, 255, 255, 0.45);
  font-size: 15px;
}

/* ====== 输入框 ====== */
.login-input :deep(.el-input__wrapper) {
  height: 58px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: none;
  transition: all 0.3s;
}

.login-input :deep(.el-input__wrapper:hover) {
  border-color: rgba(64, 158, 255, 0.4);
  background: rgba(255, 255, 255, 0.1);
}

.login-input :deep(.el-input__wrapper.is-focus) {
  border-color: #409eff;
  box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.15);
  background: rgba(255, 255, 255, 0.12);
}

.login-input :deep(.el-input__inner) {
  font-size: 15px;
  color: #fff;
}

.login-input :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.35);
}

.login-input :deep(.el-input__prefix) {
  color: rgba(255, 255, 255, 0.4);
}

/* checkBox 文字 */
.login-card :deep(.el-checkbox__label) {
  color: rgba(255, 255, 255, 0.6);
}

/* ====== 登录按钮 ====== */
.login-btn {
  width: 100%;
  height: 58px;
  border: none;
  border-radius: 14px;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 6px;
  background: linear-gradient(135deg, #4facfe, #0066ff);
  box-shadow: 0 10px 30px rgba(0, 102, 255, 0.35);
  transition: all 0.3s ease;
  margin-top: 8px;
}

.login-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 40px rgba(0, 102, 255, 0.5);
  background: linear-gradient(135deg, #6fbfff, #1a7aff);
}

.login-btn:active {
  transform: translateY(0);
}
@media (max-width: 768px) {
  .login-container { flex-direction: column; gap: 16px; padding: 20px; }
  .robot-image { width: 280px; transform: scale(1); }
  .robot-section { margin-top: 0; margin-right: 0; }
  .brand-title { font-size: 32px; letter-spacing: 4px; }
  .brand-subtitle { font-size: 14px; }
  .brand-tagline { font-size: 13px; }
  .login-content { margin-bottom: 20px; }
  .login-card { width: 100%; }
  .float-tag { display: none; }
}
</style>
