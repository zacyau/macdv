<template>
  <div class="w-full max-w-xl mx-auto px-4">
    <a-card class="shadow-sm border-gray-100" :bordered="false">
      <a-form layout="vertical">
        <a-form-item label="股票列表">
          <a-textarea
            v-model:value="inputText"
            placeholder="股票名称或代码，逗号、空格或换行分隔"
            :rows="3"
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
