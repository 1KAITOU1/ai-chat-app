<template>
  <aside class="sidebar">
    <button class="new-btn" @click="onNew">+ 新对话</button>
    <div class="list">
      <div
        v-for="conv in store.conversations"
        :key="conv.id"
        :class="['item', { active: conv.id === store.currentId }]"
        @click="onSwitch(conv.id)"
      >
        <span class="title">{{ conv.title || '新对话' }}</span>
        <button class="del" @click.stop="onDelete(conv.id)">×</button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { onMounted } from 'vue'
import { useConversationStore } from '../stores/conversation'

const store = useConversationStore()

onMounted(() => {
  store.loadConversations()
})

async function onNew() {
  await store.createConversation()
}

async function onSwitch(id) {
  await store.switchConversation(id)
}

async function onDelete(id) {
  if (confirm('删除这个对话？')) {
    await store.deleteConversation(id)
  }
}
</script>

<style scoped>
.sidebar {
  width: 260px;
  background: #f5f5f7;
  border-right: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.new-btn {
  margin: 12px;
  padding: 10px;
  background: #007aff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.new-btn:hover { background: #0066d6; }
.list {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px;
}
.item {
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 4px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.item:hover { background: #e5e5ea; }
.item.active { background: #d0e4ff; }
.title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
}
.del {
  color: #999;
  background: transparent;
  border: none;
  font-size: 18px;
  cursor: pointer;
  padding: 0 4px;
  line-height: 1;
}
.del:hover { color: #ff3b30; }
</style>