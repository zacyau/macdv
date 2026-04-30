<template>
  <div>
    <a-card class="shadow-sm border-gray-100" :bordered="false">
      <template #title>
        <div class="flex justify-between items-center">
          <span class="text-base font-semibold text-gray-800">查询结果</span>
          <span class="text-gray-400 text-xs">{{ data.updated_at }}</span>
        </div>
      </template>
      <DraggableContainer>
        <a-table
          :columns="columns"
          :data-source="tableData"
          :pagination="false"
          :row-key="(_, index) => index"
          size="middle"
          class="result-table"
        >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'macdv'">
            <div class="flex flex-col items-start gap-1">
              <span :class="macdvColor(record.macdv)">{{ record.macdv }}</span>
              <a-tag :color="macdvTagColor(record.macdv_trend)" class="status-tag">
                {{ macdvTrendText(record.macdv_trend) }}
              </a-tag>
            </div>
          </template>
          <template v-if="column.key === 'rsi14'">
            <div class="flex flex-col items-start gap-1">
              <span :class="rsiColor(record.rsi14)">{{ record.rsi14 }}</span>
              <a-tag :color="rsiTagColor(record.rsi14_signal)" class="status-tag">
                {{ rsiSignalText(record.rsi14_signal) }}
              </a-tag>
            </div>
          </template>
          <template v-if="column.key === 'recommendation'">
            <a-tag :color="recommendationColor(record.recommendation)">
              {{ record.recommendation }}
            </a-tag>
          </template>
        </template>
        </a-table>
      </DraggableContainer>
    </a-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import DraggableContainer from './DraggableContainer.vue'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const columns = [
  { title: '股票名称', dataIndex: 'stock_name', key: 'stock_name' },
  { title: '股票代码', dataIndex: 'stock_code', key: 'stock_code' },
  { title: '日期', dataIndex: 'trade_date', key: 'trade_date' },
  { title: '当前股价', dataIndex: 'current_price', key: 'current_price' },
  { title: 'MACD-V', key: 'macdv' },
  { title: 'RSI 14', key: 'rsi14' },
  { title: '买卖建议', key: 'recommendation' },
]

const tableData = computed(() => {
  return props.data.results || []
})

function macdvColor(val) {
  if (val > 0) return 'text-red-500 font-bold'
  if (val < 0) return 'text-green-500 font-bold'
  return 'text-gray-700 font-bold'
}

function macdvTrendText(trend) {
  const map = {
    momentum_peak: '动量峰值',
    strong_up: '强劲上涨',
    oscillation: '震荡',
    strong_down: '强劲下跌',
    momentum_decay: '动量衰竭',
  }
  return map[trend] || '震荡'
}

function macdvTagColor(trend) {
  if (trend === 'momentum_peak') return 'red'
  if (trend === 'strong_up') return 'orange'
  if (trend === 'strong_down') return 'cyan'
  if (trend === 'momentum_decay') return 'purple'
  return 'default'
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

function recommendationColor(rec) {
  if (rec === '左侧买点') return 'green'
  if (rec === '右侧买点') return 'blue'
  if (rec === '左侧卖点') return 'red'
  if (rec === '右侧卖点') return 'orange'
  return 'default'
}
</script>

<style scoped>
.status-tag {
  min-width: 48px;
  text-align: center;
  display: inline-block;
}
.result-table :deep(.ant-table-thead > tr > th) {
  background: #f9fafb;
  font-weight: 500;
  color: #6b7280;
  font-size: 13px;
}
.result-table :deep(.ant-table-tbody > tr > td) {
  font-size: 14px;
}
</style>
