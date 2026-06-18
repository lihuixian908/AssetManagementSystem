# 固定资产管理系统

基于 FastAPI + Vue 3 的企业固定资产全生命周期管理系统。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| ORM | SQLAlchemy 2.0 |
| 数据库 | MySQL 8.0 |
| 认证 | JWT |
| 前端框架 | Vue 3 + TypeScript |
| UI 组件 | Element Plus |
| 构建工具 | Vite |

## 功能模块

- 用户管理（CRUD / 角色 / 启用禁用 / 重置密码）
- 资产目录（设备查询 / 新增 / 编辑 / 删除 / 报废 / Excel 导入导出）
- 资产流动管理（出借 / 归还 / 变动 / 流转记录时间线）
- 二维码管理（生成 / 下载 / 手机扫码出借归还）
- 仪表盘（资产统计 / 状态分布 / 逾期提醒 / 近期操作）
- 响应式布局（PC / 平板 / 手机）

## 快速启动

### 后端

```bash
cd asset-server
pip install -r requirements.txt
python -m app.scripts.seed      # 初始化演示数据
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端

```bash
cd asset-web
npm install
npm run dev
```

访问 http://localhost:3000

## 演示账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 普通用户 | zhangsan | 123456 |
