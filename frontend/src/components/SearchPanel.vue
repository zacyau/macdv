<template>
  <div class="w-full max-w-2xl mx-auto p-4">
    <a-card title="股票批量查询" class="shadow-md">
      <a-form layout="vertical">
        <a-form-item label="股票列表">
          <a-textarea
            v-model:value="inputText"
            placeholder="请输入股票名称或股票代码，支持逗号、空格或换行分隔"
            :rows="4"
            allow-clear
          />
        </a-form-item>
        <a-form-item>
          <a-button
            type="primary"
            :loading="loading"
            :disabled="!canQuery"
            @click="handleQuery"
          >
            批量查询
          </a-button>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

defineProps({
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['query'])

const inputText = ref('')

const canQuery = computed(() => {
  return inputText.value.trim().length > 0
})

function handleQuery() {
  const raw = inputText.value.trim()
  if (!raw) return
  const queries = raw
    .split(/[,，\s\n]+/)
    .map(s => s.trim())
    .filter(s => s.length > 0)
  emit('query', queries)
}
</script>
