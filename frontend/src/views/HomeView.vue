<template>
  <div class="min-h-screen py-8">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-800">估值与技术数据</h1>
      <p class="text-gray-500 mt-2">支持沪深A股及主要ETF批量查询</p>
    </div>

    <SearchPanel :loading="loading" @query="onQuery" />

    <transition name="fade">
      <div v-if="loading" class="w-full max-w-2xl mx-auto p-4 text-center">
        <a-spin size="large" tip="数据加载中..." />
      </div>
    </transition>

    <transition name="fade">
      <div v-if="error" class="w-full max-w-2xl mx-auto p-4">
        <a-alert
          :message="error"
          type="error"
          show-icon
          closable
          @close="error = ''"
        />
      </div>
    </transition>

    <transition name="fade">
      <div v-if="result" class="mt-4 w-full max-w-5xl mx-auto">
        <IndicatorCards :data="result" />
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SearchPanel from '../components/SearchPanel.vue'
import IndicatorCards from '../components/IndicatorCards.vue'
import { batchQueryStock } from '../utils/api.js'

const loading = ref(false)
const error = ref('')
const result = ref(null)

async function onQuery(queries) {
  loading.value = true
  error.value = ''
  result.value = null
  try {
    const data = await batchQueryStock(queries)
    result.value = data
  } catch (err) {
    if (err.response) {
      error.value = err.response.data?.detail || '查询失败'
    } else {
      error.value = '网络错误，请稍后重试'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
