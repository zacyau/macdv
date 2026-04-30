<template>
  <div>
    <n-card class="shadow-sm" :bordered="false">
      <template #header>
        <div class="flex justify-between items-center">
          <span class="text-base font-semibold text-gray-800">查询结果</span>
          <span class="text-gray-400 text-xs">{{ data.updated_at }}</span>
        </div>
      </template>
      <DraggableContainer>
        <n-data-table
          :columns="visibleColumns"
          :data="tableData"
          :pagination="false"
          :row-key="(row) => row.stock_code"
          size="medium"
          class="result-table"
        />
      </DraggableContainer>
    </n-card>
  </div>
</template>

<script setup>
import { h, computed, ref, onMounted, onUnmounted } from 'vue'
import { NCard, NDataTable, NTag } from 'naive-ui'
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

function macdvTagProps(trend) {
  if (trend === 'momentum_peak') return { type: 'error', bordered: false }
  if (trend === 'strong_up') return { type: 'warning', bordered: false }
  if (trend === 'strong_down') return { color: { color: '#e6fffb', textColor: '#08979c', borderColor: '#87e8de' }, bordered: true }
  if (trend === 'momentum_decay') return { color: { color: '#f9f0ff', textColor: '#722ed1', borderColor: '#d3adf7' }, bordered: true }
  return { bordered: false }
}

function rsiColor(val) {
  if (val > 70) return 'text-red-500 font-bold'
  if (val < 30) return 'text-green-500 font-bold'
  return 'text-gray-700 font-bold'
}

function rsiTagProps(signal) {
  if (signal === 'overbought') return { type: 'error', bordered: false }
  if (signal === 'oversold') return { type: 'success', bordered: false }
  return { bordered: false }
}

function rsiSignalText(signal) {
  if (signal === 'overbought') return '超买'
  if (signal === 'oversold') return '超卖'
  return '中性'
}

function recommendationTagProps(rec) {
  if (rec === '左侧买点') return { type: 'success', bordered: false }
  if (rec === '右侧买点') return { type: 'info', bordered: false }
  if (rec === '左侧卖点') return { type: 'error', bordered: false }
  if (rec === '右侧卖点') return { type: 'warning', bordered: false }
  return { bordered: false }
}

const allColumns = [
  { title: '股票名称', key: 'stock_name', minWidth: 80 },
  { title: '股票代码', key: 'stock_code', minWidth: 80 },
  { title: '日期', key: 'trade_date', minWidth: 90, hideOnMobile: true },
  { title: '当前股价', key: 'current_price', minWidth: 80, hideOnMobile: true },
  {
    title: 'MACD-V',
    key: 'macdv',
    minWidth: 120,
    render(row) {
      return h('div', { class: 'flex flex-col items-start gap-1' }, [
        h('span', { class: macdvColor(row.macdv) }, row.macdv),
        h(NTag, { size: 'small', ...macdvTagProps(row.macdv_trend) }, { default: () => macdvTrendText(row.macdv_trend) })
      ])
    }
  },
  {
    title: 'RSI 14',
    key: 'rsi14',
    minWidth: 100,
    render(row) {
      return h('div', { class: 'flex flex-col items-start gap-1' }, [
        h('span', { class: rsiColor(row.rsi14) }, row.rsi14),
        h(NTag, { size: 'small', ...rsiTagProps(row.rsi14_signal) }, { default: () => rsiSignalText(row.rsi14_signal) })
      ])
    }
  },
  {
    title: '买卖建议',
    key: 'recommendation',
    minWidth: 90,
    render(row) {
      return h(NTag, { size: 'small', ...recommendationTagProps(row.recommendation) }, { default: () => row.recommendation })
    }
  }
]

const visibleColumns = computed(() => {
  if (isMobile.value) {
    return allColumns.filter(col => !col.hideOnMobile)
  }
  return allColumns
})

const tableData = computed(() => {
  return props.data.results || []
})
</script>

<style scoped>
.result-table :deep(.n-data-table-th) {
  background: #f9fafb;
  font-weight: 500;
  color: #6b7280;
  font-size: 13px;
}
.result-table :deep(.n-data-table-td) {
  font-size: 14px;
}
</style>
