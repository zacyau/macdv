<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="text-center mb-6 pt-10">
      <h1 class="text-4xl font-bold text-gray-900 tracking-tight">估值与技术数据</h1>
      <p class="text-gray-400 mt-3 text-sm">支持沪深A股及主要ETF批量查询macdv、rsi 指标</p>
      <a-button
        type="link"
        size="small"
        class="mt-2 text-gray-400 hover:text-gray-600"
        @click="guideVisible = true"
      >
        使用说明
      </a-button>
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
      <div v-if="result" class="mt-6 w-full max-w-6xl mx-auto px-4">
        <IndicatorCards :data="result" />
      </div>
    </transition>

    <a-modal
      v-model:visible="guideVisible"
      title="使用说明"
      :footer="null"
      width="520px"
    >
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
          <ul class="list-disc pl-5 space-y-2 text-sm">
            <li>
              <span class="text-gray-400 font-medium">观望</span>
              <span class="ml-1">MACD-V 在 ±50 内，无论 RSI 如何，直接观望</span>
            </li>
            <li>
              <span class="text-green-500 font-medium">找机会买</span>
              <span class="ml-1">RSI &lt; 30 且 MACD-V 在 +50 上方或 -150 下方</span>
            </li>
            <li>
              <span class="text-red-500 font-medium">找机会卖</span>
              <span class="ml-1">RSI &gt; 70 且 MACD-V 在 +150 上方或 +50 下方</span>
            </li>
          </ul>
        </div>
        <div class="pt-2 border-t border-gray-100">
          <p class="text-xs text-gray-400">以上信号仅供参考，不构成投资建议。</p>
        </div>
      </div>
    </a-modal>
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
const guideVisible = ref(false)

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
