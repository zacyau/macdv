<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="text-center mb-6 pt-6 sm:pt-8 lg:pt-10">
      <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 tracking-tight">趋势信号</h1>
      <p class="text-gray-400 mt-2 sm:mt-3 text-xs sm:text-sm">支持沪深A股及主要ETF批量查询macdv、rsi 指标</p>
      <n-button
        size="small"
        class="mt-3"
        @click="guideExpanded = !guideExpanded"
      >
        <template #icon>
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M12 2a10 10 0 100 20 10 10 0 000-20z" />
          </svg>
        </template>
        使用说明
      </n-button>
    </div>

    <transition name="fade">
      <div v-if="guideExpanded" class="w-full max-w-xl mx-auto px-3 sm:px-4 mb-4">
        <n-card size="small" class="shadow-sm" :bordered="false">
          <div class="space-y-4 text-gray-600 leading-relaxed">
            <div>
              <p class="font-semibold text-gray-800 mb-2">指标说明</p>
              <ul class="list-disc pl-5 space-y-1 text-sm">
                <li><span class="font-medium">MACD-V</span>：衡量价格动量与波动率的比值，反映趋势强度</li>
                <li><span class="font-medium">RSI 14</span>：相对强弱指标，衡量超买超卖状态</li>
              </ul>
            </div>
            <div>
              <p class="font-semibold text-gray-800 mb-2">交易信号</p>
              <ul class="pl-1 space-y-2 text-sm">
                <li class="flex items-start gap-1">
                  <n-tag size="small" type="info" :bordered="false">右侧买点</n-tag>
                  <span>MACD-V：+50 ~ +150（确认强势），RSI &lt; 30（超卖区）</span>
                </li>
                <li class="flex items-start gap-1">
                  <n-tag size="small" type="success" :bordered="false">左侧买点</n-tag>
                  <span>MACD-V：&lt; -150（恐慌性超卖），RSI &lt; 30（超卖区）</span>
                </li>
                <li class="flex items-start gap-1">
                  <n-tag size="small" type="error" :bordered="false">左侧卖点</n-tag>
                  <span>MACD-V：&gt; +150（情绪过热），RSI &gt; 70（超买区）</span>
                </li>
                <li class="flex items-start gap-1">
                  <n-tag size="small" type="warning" :bordered="false">右侧卖点</n-tag>
                  <span>MACD-V：&lt; +50（趋势转弱），RSI &gt; 70（超买区）</span>
                </li>
                <li class="flex items-start gap-1">
                  <n-tag size="small" :bordered="false">观望</n-tag>
                  <span>MACD-V：-50 ~ +50（无趋势区），无论 RSI 如何都是噪音</span>
                </li>
              </ul>
            </div>
            <div class="pt-2 border-t border-gray-100">
              <p class="text-xs text-gray-400">以上信号仅供参考，不构成投资建议。</p>
            </div>
          </div>
        </n-card>
      </div>
    </transition>

    <SearchPanel :loading="loading" @query="onQuery" />

    <transition name="fade">
      <div v-if="loading" class="w-full max-w-2xl mx-auto p-4 text-center">
        <n-spin size="large">
          <template #description>
            <span class="text-gray-400">数据加载中...</span>
          </template>
        </n-spin>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="error" class="w-full max-w-2xl mx-auto p-2 sm:p-4">
        <n-alert
          :title="error"
          type="error"
          closable
          @close="error = ''"
        />
      </div>
    </transition>

    <transition name="fade">
      <div v-if="result" class="mt-4 sm:mt-6 w-full max-w-6xl mx-auto px-2 sm:px-4">
        <IndicatorCards :data="result" />
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { NButton, NSpin, NAlert, NCard } from 'naive-ui'
import SearchPanel from '../components/SearchPanel.vue'
import IndicatorCards from '../components/IndicatorCards.vue'
import { batchQueryStock } from '../utils/api.js'

const loading = ref(false)
const error = ref('')
const result = ref(null)
const guideExpanded = ref(false)

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
