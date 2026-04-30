<template>
  <div class="table-container">
    <DraggableContainer>
      <a-table
        :columns="visibleColumns"
        :data-source="data.results || []"
        :pagination="false"
        :row-key="(_, index) => index"
        size="middle"
        class="result-table"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'macdv'">
            <div class="cell-stack">
              <span :class="macdvColor(record.macdv)">{{ record.macdv }}</span>
              <a-tag :color="macdvTagColor(record.macdv_trend)" class="status-tag">
                {{ macdvTrendText(record.macdv_trend) }}
              </a-tag>
            </div>
          </template>
          <template v-if="column.key === 'rsi14'">
            <div class="cell-stack">
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
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import DraggableContainer from './DraggableContainer.vue'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const windowWidth = ref(window.innerWidth)
function onResize() {
  windowWidth.value = window.innerWidth
}
onMounted(() => window.addEventListener('resize', onResize))
onUnmounted(() => window.removeEventListener('resize', onResize))

const isMobile = computed(() => windowWidth.value < 640)

const allColumns = [
  { title: '股票名称', dataIndex: 'stock_name', key: 'stock_name', minWidth: 80 },
  { title: '股票代码', dataIndex: 'stock_code', key: 'stock_code', minWidth: 80 },
  { title: '日期', dataIndex: 'trade_date', key: 'trade_date', hideOnMobile: true },
  { title: '当前股价', dataIndex: 'current_price', key: 'current_price', hideOnMobile: true },
  { title: 'MACD-V', key: 'macdv' },
  { title: 'RSI 14', key: 'rsi14' },
  { title: '买卖建议', key: 'recommendation' },
]

const visibleColumns = computed(() => {
  if (isMobile.value) {
    return allColumns.filter(col => !col.hideOnMobile)
  }
  return allColumns
})

function macdvColor(val) {
  if (val > 0) return 'text-red font-bold'
  if (val < 0) return 'text-green font-bold'
  return 'text-gray font-bold'
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
  if (val > 70) return 'text-red font-bold'
  if (val < 30) return 'text-green font-bold'
  return 'text-gray font-bold'
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
.table-container {
  overflow-x: auto;
}

.cell-stack {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.text-red { color: #ef4444; }
.text-green { color: #10b981; }
.text-gray { color: #374151; }
.font-bold { font-weight: 700; }

.status-tag {
  min-width: 48px;
  text-align: center;
  display: inline-block;
}

.result-table :deep(.ant-table-thead > tr > th) {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
  font-size: 0.85rem;
  border-bottom: 2px solid #e5e7eb;
}

.result-table :deep(.ant-table-tbody > tr > td) {
  font-size: 0.9rem;
  border-bottom: 1px solid #f3f4f6;
}

.result-table :deep(.ant-table-tbody > tr:hover > td) {
  background: #f9fafb;
}
</style>
