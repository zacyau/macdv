<template>
  <div class="history-wrapper">
    <div class="history-card">
      <div class="history-head">
        <h3 class="history-title">历史查询</h3>
      </div>
      <a-list
        v-if="history.length"
        :data-source="history"
        size="small"
        class="history-list"
      >
        <template #renderItem="{ item }">
          <a-list-item class="history-item">
            <a-button type="link" class="history-link" @click="handleClick(item)">
              {{ item.stock_name }} ({{ item.stock_code }}) - {{ item.trade_date }}
            </a-button>
          </a-list-item>
        </template>
      </a-list>
      <a-empty v-else description="暂无历史记录" class="history-empty" />
    </div>
  </div>
</template>

<script setup>
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

<style scoped>
.history-wrapper {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px 16px;
}
.history-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 14px 18px;
}
.history-head {
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eef1f6;
}
.history-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1a335e;
  margin: 0;
}
.history-list :deep(.ant-list-items) {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.history-item {
  padding: 0 !important;
  border-bottom: none !important;
}
.history-link {
  font-size: 0.78rem;
  padding: 2px 8px;
  color: #1a335e;
}
.history-link:hover {
  color: #0d1c3e;
}
.history-empty {
  padding: 12px 0;
}
</style>
