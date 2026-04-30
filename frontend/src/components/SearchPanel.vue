<template>
  <div class="w-full max-w-full sm:max-w-xl mx-auto px-3 sm:px-4">
    <n-card class="shadow-sm" :bordered="false">
      <n-form label-placement="top">
        <n-form-item label="股票列表">
          <n-input
            v-model:value="inputText"
            type="textarea"
            placeholder="股票名称或代码，逗号、空格或换行分隔"
            :rows="3"
            clearable
          />
        </n-form-item>
        <n-form-item :show-label="false">
          <n-button
            type="primary"
            :loading="loading"
            :disabled="!canQuery"
            class="w-full sm:w-auto"
            @click="handleQuery"
          >
            批量查询
          </n-button>
        </n-form-item>
      </n-form>
    </n-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { NCard, NForm, NFormItem, NInput, NButton } from 'naive-ui'

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
