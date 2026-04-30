<template>
  <div class="w-full max-w-2xl mx-auto p-4">
    <a-card title="历史查询" class="shadow-md">
      <a-list
        v-if="history.length"
        :data-source="history"
        size="small"
      >
        <template #renderItem="{ item }">
          <a-list-item>
            <a-button type="link" @click="handleClick(item)">
              {{ item.stock_name }} ({{ item.stock_code }}) - {{ item.trade_date }}
            </a-button>
          </a-list-item>
        </template>
      </a-list>
      <a-empty v-else description="暂无历史记录" />
    </a-card>
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
