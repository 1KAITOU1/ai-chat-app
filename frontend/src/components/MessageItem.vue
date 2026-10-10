<template>
  <div :class="['msg', message.role]">
    <div class="bubble">
      <div v-if="message.role === 'assistant'" 
           class="markdown-body" 
           v-html="renderedContent"></div>
      <div v-else class="plain-text">{{ message.content }}</div>
    </div>
    <button v-if="message.role === 'assistant'" 
            class="copy-btn" 
            @click="copyContent">
      {{ copied ? '已复制' : '复制' }}
    </button>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import DOMPurify from 'dompurify'
import 'highlight.js/styles/github.css'

const props = defineProps({
  message: { type: Object, required: true }
})

const copied = ref(false)

// 配置 marked：代码块用 highlight.js 高亮
marked.setOptions({
  highlight: function (code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true,
  gfm: true
})

const renderedContent = computed(() => {
  const raw = marked.parse(props.message.content || '')
  return DOMPurify.sanitize(raw)
})

async function copyContent() {
  try {
    await navigator.clipboard.writeText(props.message.content)
    copied.value = true
    setTimeout(() => { copied.value = false }, 1500)
  } catch (e) {
    console.error('复制失败', e)
  }
}
</script>

<style scoped>
.msg { margin: 12px 0; display: flex; flex-direction: column; }
.msg.user { align-items: flex-end; }
.msg.assistant { align-items: flex-start; }

.bubble {
  max-width: 75%;
  padding: 10px 16px;
  border-radius: 12px;
  white-space: pre-wrap;
  word-break: break-word;
}
.msg.user .bubble { background: #007aff; color: white; }
.msg.assistant .bubble { background: #f5f5f7; color: #1d1d1f; }

.plain-text { white-space: pre-wrap; }

/* Markdown 内容样式 */
.markdown-body :deep(pre) {
  background: #f6f8fa;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
}
.markdown-body :deep(code) {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
}
.markdown-body :deep(p) { margin: 6px 0; }
.markdown-body :deep(ul), .markdown-body :deep(ol) { padding-left: 24px; }
.markdown-body :deep(table) {
  border-collapse: collapse;
  margin: 8px 0;
}
.markdown-body :deep(th), .markdown-body :deep(td) {
  border: 1px solid #ddd;
  padding: 6px 10px;
}

.copy-btn {
  margin-top: 4px;
  font-size: 12px;
  color: #666;
  background: transparent;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 2px 10px;
  cursor: pointer;
}
.copy-btn:hover { background: #f0f0f0; }
</style>