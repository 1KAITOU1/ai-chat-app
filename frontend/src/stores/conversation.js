import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useConversationStore = defineStore('conversation', () => {
  const conversations = ref([])
  const currentId = ref(null)
  const messages = ref([])
  const loading = ref(false)

  async function loadConversations() {
    const res = await fetch('/api/conversations')
    conversations.value = await res.json()
  }

  async function createConversation() {
    const res = await fetch('/api/conversations', { method: 'POST' })
    const conv = await res.json()
    conversations.value.unshift(conv)
    currentId.value = conv.id
    messages.value = []
    return conv
  }

  async function switchConversation(id) {
    currentId.value = id
    const res = await fetch(`/api/conversations/${id}/messages`)
    messages.value = await res.json()
  }

  async function deleteConversation(id) {
    await fetch(`/api/conversations/${id}`, { method: 'DELETE' })
    conversations.value = conversations.value.filter(c => c.id !== id)
    if (currentId.value === id) {
      currentId.value = null
      messages.value = []
    }
  }

  return {
    conversations,
    currentId,
    messages,
    loading,
    loadConversations,
    createConversation,
    switchConversation,
    deleteConversation
  }
})