<template>
  <router-view />
</template>

<script setup lang="ts">
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.el-card {
  border-radius: 12px !important;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08) !important;
}

.el-button {
  border-radius: 8px;
}

.el-input .el-input__wrapper,
.el-select .el-select__wrapper,
.el-input-number .el-input__wrapper {
  border-radius: 8px;
}

.el-dialog {
  border-radius: 12px;
}
</style>