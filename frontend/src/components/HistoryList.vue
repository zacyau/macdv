<template>
  <div class="w-full max-w-2xl mx-auto p-4">
    <n-card title="历史查询" class="shadow-md">
      <n-list v-if="history.length" bordered>
        <n-list-item v-for="(item, index) in history" :key="index">
          <n-button text type="primary" @click="handleClick(item)">
            {{ item.stock_name }} ({{ item.stock_code }}) - {{ item.trade_date }}
          </n-button>
        </n-list-item>
      </n-list>
      <n-empty v-else description="暂无历史记录" />
    </n-card>
  </div>
</template>

<script setup>
import { NCard, NList, NListItem, NButton, NEmpty } from 'naive-ui'

defineProps({
  history: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['select'])

function handleClick(item) {
  emit('select', item)
}
</script>
