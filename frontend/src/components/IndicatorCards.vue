<template>
  <div class="p-4">
    <a-card class="shadow-md">
      <template #title>
        <div class="flex justify-between items-center">
          <div>
            <span class="text-xl font-bold mr-2">{{ data.stock_name }}</span>
            <span class="text-gray-500">{{ data.stock_code }}</span>
          </div>
          <div class="text-gray-500">{{ data.trade_date }}</div>
        </div>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <a-card class="text-center">
          <div class="text-gray-500 text-sm">当前股价</div>
          <div class="text-2xl font-bold text-blue-600">{{ data.current_price }}</div>
        </a-card>
        <a-card class="text-center">
          <div class="text-gray-500 text-sm">MACD-V</div>
          <div class="text-2xl font-bold" :class="macdvColor">{{ data.macdv }}</div>
          <a-tag :color="macdvTagColor">{{ macdvTrendText }}</a-tag>
        </a-card>
        <a-card class="text-center">
          <div class="text-gray-500 text-sm">RSI 14</div>
          <div class="text-2xl font-bold" :class="rsiColor">{{ data.rsi14 }}</div>
          <a-tag :color="rsiTagColor">{{ rsiSignalText }}</a-tag>
        </a-card>
      </div>
    </a-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const macdvColor = computed(() => {
  if (props.data.macdv > 0) return 'text-red-500'
  if (props.data.macdv < 0) return 'text-green-500'
  return 'text-gray-700'
})

const macdvTagColor = computed(() => {
  if (props.data.macdv_trend === 'up') return 'red'
  if (props.data.macdv_trend === 'down') return 'green'
  return 'default'
})

const macdvTrendText = computed(() => {
  if (props.data.macdv_trend === 'up') return '上升'
  if (props.data.macdv_trend === 'down') return '下降'
  return '平稳'
})

const rsiColor = computed(() => {
  if (props.data.rsi14 > 70) return 'text-red-500'
  if (props.data.rsi14 < 30) return 'text-green-500'
  return 'text-gray-700'
})

const rsiTagColor = computed(() => {
  if (props.data.rsi14_signal === 'overbought') return 'red'
  if (props.data.rsi14_signal === 'oversold') return 'green'
  return 'default'
})

const rsiSignalText = computed(() => {
  if (props.data.rsi14_signal === 'overbought') return '超买'
  if (props.data.rsi14_signal === 'oversold') return '超卖'
  return '中性'
})
</script>
