cd ~/ai-chat-app
cat > README.md << 'EOF'
# AI Chat App

基于 Ollama + FastAPI + Vue 3 的本地 AI 对话应用，支持流式输出。

## 技术栈

- 后端：FastAPI + Python 3.11
- 前端：Vue 3 + Vite
- 大模型：Ollama（qwen2.5:7b）
- 部署：Docker Compose + GitHub Actions CI

## 快速开始

\`\`\`bash
# 1. 在 Linux 上启动 Ollama、backend、frontend
cd /opt/ai-chat-app
docker compose pull
docker compose up -d

# 2. 首次拉取模型
docker exec -it ollama ollama pull qwen2.5:7b
\`\`\`

访问 http://localhost

## 开发

- Windows 上开发前端：`cd frontend && npm install && npm run dev`
- Vite 通过 proxy 将 /api 转发到 Linux 的 8000 端口

## CI/CD

- 推送到 main 分支，GitHub Actions 自动构建镜像并推送到 GHCR
- 在 Linux 上执行 `docker compose pull && docker compose up -d` 完成部署

## 目录结构

\`\`\`
backend/    FastAPI 后端
frontend/   Vue 3 前端
docker-compose.yml
\`\`\`
EOF

git add README.md
git commit -m "add README"
git push
