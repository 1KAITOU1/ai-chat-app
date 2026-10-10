<template>
  <div class="app">
    <Sidebar />
    <ChatView />
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue'
import ChatView from './views/ChatView.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
.app {
  display: flex;
  height: 100vh;
}
</style>