<template>
  <div class="p-4">
    <a-card class="shadow-md">
      <template #title>
        <div class="flex justify-between items-center">
          <span class="text-lg font-bold">查询结果</span>
          <span class="text-gray-500 text-sm">{{ data.updated_at }}</span>
        </div>
      </template>
      <a-table
        :columns="columns"
        :data-source="tableData"
        :pagination="false"
        row-key="stock_code"
        size="middle"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'macdv'">
            <span :class="macdvColor(record.macdv)">{{ record.macdv }}</span>
            <a-tag :color="macdvTagColor(record.macdv_trend)">
              {{ macdvTrendText(record.macdv_trend) }}
            </a-tag>
          </template>
          <template v-if="column.key === 'rsi14'">
            <span :class="rsiColor(record.rsi14)">{{ record.rsi14 }}</span>
            <a-tag :color="rsiTagColor(record.rsi14_signal)">
              {{ rsiSignalText(record.rsi14_signal) }}
            </a-tag>
          </template>
          <template v-if="column.key === 'error'">
            <span v-if="record.error" class="text-red-500">{{ record.error }}</span>
            <span v-else class="text-green-500">成功</span>
          </template>
        </template>
      </a-table>
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

const columns = [
  { title: '股票名称', dataIndex: 'stock_name', key: 'stock_name' },
  { title: '股票代码', dataIndex: 'stock_code', key: 'stock_code' },
  { title: '交易日期', dataIndex: 'trade_date', key: 'trade_date' },
  { title: '当前股价', dataIndex: 'current_price', key: 'current_price' },
  { title: 'MACD-V', key: 'macdv' },
  { title: 'RSI 14', key: 'rsi14' },
  { title: '状态', key: 'error' },
]

const tableData = computed(() => {
  return props.data.results || []
})

function macdvColor(val) {
  if (val > 0) return 'text-red-500 font-bold'
  if (val < 0) return 'text-green-500 font-bold'
  return 'text-gray-700 font-bold'
}

function macdvTagColor(trend) {
  if (trend === 'up') return 'red'
  if (trend === 'down') return 'green'
  return 'default'
}

function macdvTrendText(trend) {
  if (trend === 'up') return '上升'
  if (trend === 'down') return '下降'
  return '平稳'
}

function rsiColor(val) {
  if (val > 70) return 'text-red-500 font-bold'
  if (val < 30) return 'text-green-500 font-bold'
  return 'text-gray-700 font-bold'
}

function rsiTagColor(signal) {
  if (signal === 'overbought') return 'red'
  if (signal === 'oversold') return 'green'
  return 'default'
}

function rsiSignalText(signal) {
  if (signal === 'overbought') return '超买'
  if (signal === 'oversold') return '超卖'
  return '中性'
}
</script>
