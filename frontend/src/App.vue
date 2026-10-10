<template>
  <div class="chat-container">
    <div class="messages" ref="messagesRef">
      <MessageItem v-for="(msg, i) in messages" :key="i" :message="msg" />
    </div>
    <div class="input-area">
      <input
        v-model="input"
        @keyup.enter="send"
        placeholder="输入消息..."
        :disabled="loading"
      />
      <button v-if="!loading" @click="send" :disabled="!input.trim()">
        发送
      </button>
      <button v-else class="stop-btn" @click="stopGeneration">
        停止
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import MessageItem from './components/MessageItem.vue'

const messages = ref([])
const input = ref('')
const loading = ref(false)
const messagesRef = ref(null)

let currentController = null

async function send() {
  const text = input.value.trim()
  if (!text) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true

  const aiMsg = { role: 'assistant', content: '' }
  messages.value.push(aiMsg)

  currentController = new AbortController()

  try {
    const res = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: messages.value
          .slice(0, -1)
          .map(m => ({ role: m.role, content: m.content }))
      }),
      signal: currentController.signal
    })

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`)
    }

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
    if (e.name === 'AbortError') {
      aiMsg.content += '\n\n_[已停止生成]_'
    } else {
      aiMsg.content += `\n\n**[错误]** ${e.message}`
    }
  } finally {
    loading.value = false
    currentController = null
  }
}

function stopGeneration() {
  if (currentController) {
    currentController.abort()
  }
}
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.input-area {
  display: flex;
  padding: 16px;
  gap: 8px;
  border-top: 1px solid #eee;
}

.input-area input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
}

.input-area input:focus {
  border-color: #007aff;
}

.input-area button {
  padding: 10px 24px;
  background: #007aff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.input-area button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.stop-btn {
  background: #ff3b30 !important;
}
</style>