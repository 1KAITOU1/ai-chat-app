<template>
  <div class="chat-container">
    <div class="messages" ref="messagesRef">
      <div v-for="(msg, i) in messages" :key="i" :class="['msg', msg.role]">
        <div class="bubble">{{ msg.content }}</div>
      </div>
    </div>
    <div class="input-area">
      <input v-model="input" @keyup.enter="send" placeholder="输入消息..." :disabled="loading" />
      <button @click="send" :disabled="loading || !input.trim()">
        {{ loading ? '生成中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const messages = ref([])
const input = ref('')
const loading = ref(false)
const messagesRef = ref(null)

async function send() {
  const text = input.value.trim()
  if (!text) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true

  const aiMsg = { role: 'assistant', content: '' }
  messages.value.push(aiMsg)

  try {
    const res = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: messages.value.slice(0, -1).map(m => ({
          role: m.role, content: m.content
        }))
      })
    })

    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          if (data === '[DONE]') break
          aiMsg.content += data
          await nextTick()
          messagesRef.value?.scrollTo(0, messagesRef.value.scrollHeight)
        }
      }
    }
  } catch (e) {
    aiMsg.content += '\n[错误] 请求失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chat-container { max-width: 800px; margin: 0 auto; height: 100vh; display: flex; flex-direction: column; }
.messages { flex: 1; overflow-y: auto; padding: 20px; }
.msg { margin: 10px 0; display: flex; }
.msg.user { justify-content: flex-end; }
.bubble { max-width: 70%; padding: 10px 16px; border-radius: 12px; white-space: pre-wrap; word-break: break-word; }
.msg.user .bubble { background: #007aff; color: white; }
.msg.assistant .bubble { background: #f0f0f0; color: #333; }
.input-area { display: flex; padding: 16px; gap: 8px; border-top: 1px solid #eee; }
.input-area input { flex: 1; padding: 10px 14px; border: 1px solid #ddd; border-radius: 8px; outline: none; }
.input-area button { padding: 10px 24px; background: #007aff; color: white; border: none; border-radius: 8px; cursor: pointer; }
.input-area button:disabled { opacity: 0.5; }
</style>