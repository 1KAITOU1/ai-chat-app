<template>
  <div class="chat-container">
    <div class="messages" ref="messagesRef">
      <div v-if="!store.currentId" class="empty">
        点击左侧「新对话」开始聊天
      </div>
      <MessageItem
        v-for="(msg, i) in store.messages"
        :key="i"
        :message="msg"
      />
    </div>
    <div class="input-area">
      <input
        v-model="input"
        @keyup.enter="send"
        placeholder="输入消息..."
        :disabled="store.loading || !store.currentId"
      />
      <button
        v-if="!store.loading"
        @click="send"
        :disabled="!input.trim() || !store.currentId"
      >
        发送
      </button>
      <button v-else class="stop-btn" @click="stopGeneration">
        停止
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick } from 'vue'
import MessageItem from '../components/MessageItem.vue'
import { useConversationStore } from '../stores/conversation'

const store = useConversationStore()
const input = ref('')
const messagesRef = ref(null)

let currentController = null

async function send() {
  const text = input.value.trim()
  if (!text) return
  if (!store.currentId) {
    alert('请先点击左侧「+ 新对话」创建会话')
    return
  }

  console.log('DEBUG sending conversation_id =', store.currentId)

  store.messages.push({ role: 'user', content: text })
  input.value = ''
  store.loading = true

  const aiMsg = reactive({ role: 'assistant', content: '' })
  store.messages.push(aiMsg)

  currentController = new AbortController()

  try {
    const payload = {
      conversation_id: store.currentId,
      messages: [{ role: 'user', content: text }]
    }
    console.log('DEBUG payload =', JSON.stringify(payload))

    const res = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: currentController.signal
    })

    if (!res.ok) throw new Error(`HTTP ${res.status}`)

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

    await store.loadConversations()
  } catch (e) {
    if (e.name === 'AbortError') {
      aiMsg.content += '\n\n_[已停止生成]_'
    } else {
      aiMsg.content += `\n\n**[错误]** ${e.message}`
    }
  } finally {
    store.loading = false
    currentController = null
  }
}

function stopGeneration() {
  if (currentController) currentController.abort()
}
</script>

<style scoped>
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}
.empty {
  text-align: center;
  color: #999;
  margin-top: 40vh;
  font-size: 14px;
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