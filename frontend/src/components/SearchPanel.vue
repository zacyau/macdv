<template>
  <div class="w-full max-w-2xl mx-auto p-4">
    <a-card title="股票查询" class="shadow-md">
      <a-form layout="vertical">
        <a-form-item label="股票名称">
          <a-input
            v-model:value="nameInput"
            placeholder="请输入股票名称（支持模糊查询）"
            allow-clear
            @change="onNameChange"
          />
        </a-form-item>
        <a-form-item label="股票代码">
          <a-input
            v-model:value="codeInput"
            placeholder="请输入股票代码"
            allow-clear
            @change="onCodeChange"
          />
        </a-form-item>
        <a-form-item>
          <a-button
            type="primary"
            :loading="loading"
            :disabled="!canQuery"
            @click="handleQuery"
          >
            查询
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

const nameInput = ref('')
const codeInput = ref('')

const canQuery = computed(() => {
  return nameInput.value.trim().length > 0 || codeInput.value.trim().length > 0
})

let nameTimer = null
let codeTimer = null

function onNameChange() {
  clearTimeout(nameTimer)
  nameTimer = setTimeout(() => {
    if (nameInput.value.trim()) {
      codeInput.value = ''
    }
  }, 500)
}

function onCodeChange() {
  clearTimeout(codeTimer)
  codeTimer = setTimeout(() => {
    if (codeInput.value.trim()) {
      nameInput.value = ''
    }
  }, 500)
}

function handleQuery() {
  const params = {}
  if (codeInput.value.trim()) {
    params.stock_code = codeInput.value.trim()
  } else if (nameInput.value.trim()) {
    params.stock_name = nameInput.value.trim()
  }
  emit('query', params)
}
</script>
