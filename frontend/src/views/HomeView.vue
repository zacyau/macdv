<template>
  <div class="app">
    <header class="header">
      <h1>趋势信号</h1>
      <p class="subtitle">基于 MACD-V 与 RSI 指标的买卖信号研判工具</p>
    </header>

    <main class="main">
      <section class="search-section">
        <a-form layout="vertical">
          <div class="search-box">
            <div class="input-group full-width">
              <a-form-item label="股票列表">
                <a-textarea
                  v-model:value="inputText"
                  placeholder="股票名称或代码，逗号、空格或换行分隔"
                  :rows="3"
                  allow-clear
                  class="custom-input"
                />
              </a-form-item>
            </div>
            <div class="input-group">
              <a-form-item>
                <button
                  class="btn btn-primary"
                  :disabled="!canQuery || loading"
                  @click="handleQuery"
                >
                  {{ loading ? '查询中...' : '批量查询' }}
                </button>
              </a-form-item>
            </div>
          </div>
        </a-form>
      </section>

      <transition name="fade">
        <section v-if="error" class="error-section">
          <a-alert
            :message="error"
            type="error"
            show-icon
            closable
            @close="error = ''"
          />
        </section>
      </transition>

      <transition name="fade">
        <section v-if="result" class="result-section">
          <div class="result-header">
            <div class="result-header-top">
              <h2>查询结果</h2>
              <span class="result-time">{{ result.updated_at }}</span>
            </div>
          </div>
          <IndicatorCards :data="result" />
        </section>
      </transition>

      <section class="guide-section">
        <button class="btn btn-guide" @click="guideExpanded = !guideExpanded">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M12 2a10 10 0 100 20 10 10 0 000-20z" />
          </svg>
          使用说明
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" :class="{ 'arrow-rotate': guideExpanded }">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <transition name="fade">
          <div v-if="guideExpanded" class="guide-content">
            <div class="guide-block">
              <h3>指标说明</h3>
              <ul>
                <li><strong>MACD-V</strong>：衡量价格动量与波动率的比值，反映趋势强度</li>
                <li><strong>RSI 14</strong>：相对强弱指标，衡量超买超卖状态</li>
              </ul>
            </div>
            <div class="guide-block">
              <h3>交易信号</h3>
              <ul class="signal-list">
                <li>
                  <a-tag color="blue">右侧买点</a-tag>
                  <span>MACD-V：+50 ~ +150（确认强势），RSI &lt; 30（超卖区）</span>
                </li>
                <li>
                  <a-tag color="green">左侧买点</a-tag>
                  <span>MACD-V：&lt; -150（恐慌性超卖），RSI &lt; 30（超卖区）</span>
                </li>
                <li>
                  <a-tag color="red">左侧卖点</a-tag>
                  <span>MACD-V：&gt; +150（情绪过热），RSI &gt; 70（超买区）</span>
                </li>
                <li>
                  <a-tag color="orange">右侧卖点</a-tag>
                  <span>MACD-V：&lt; +50（趋势转弱），RSI &gt; 70（超买区）</span>
                </li>
                <li>
                  <a-tag>观望</a-tag>
                  <span>MACD-V：-50 ~ +50（无趋势区），无论 RSI 如何都是噪音</span>
                </li>
              </ul>
            </div>
            <div class="guide-disclaimer">
              以上信号仅供参考，不构成投资建议。
            </div>
          </div>
        </transition>
      </section>
    </main>

    <footer class="footer">
      <p>数据来源: baostock | 仅供参考，不构成投资建议</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import IndicatorCards from '../components/IndicatorCards.vue'
import { batchQueryStock } from '../utils/api.js'

const inputText = ref('')
const loading = ref(false)
const error = ref('')
const result = ref(null)
const guideExpanded = ref(false)

const canQuery = computed(() => {
  return inputText.value.trim().length > 0
})

async function handleQuery() {
  const raw = inputText.value.trim()
  if (!raw) return
  const queries = raw
    .split(/[,，\s\n]+/)
    .map(s => s.trim())
    .filter(s => s.length > 0)

  loading.value = true
  error.value = ''
  result.value = null
  try {
    const data = await batchQueryStock(queries)
    result.value = data
  } catch (err) {
    if (err.response) {
      error.value = err.response.data?.detail || '查询失败'
    } else {
      error.value = '网络错误，请稍后重试'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  text-align: center;
  padding: 40px 20px 30px;
  color: #1f2937;
}

.header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: #1f2937;
}

.subtitle {
  font-size: 1.1rem;
  color: #6b7280;
}

.main {
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 0 20px 40px;
}

.search-section {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  margin-bottom: 24px;
}

.search-box {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 20px;
  align-items: end;
}

.input-group.full-width {
  grid-column: 1 / -1;
}

.input-group :deep(.ant-form-item-label > label) {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
}

.input-group :deep(.ant-input) {
  padding: 10px 14px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.input-group :deep(.ant-input:focus),
.input-group :deep(.ant-input-focused) {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.btn {
  padding: 10px 24px;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  height: 40px;
  line-height: 1;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(99, 102, 241, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-guide {
  background: #f3f4f6;
  color: #374151;
  padding: 8px 16px;
  font-size: 0.9rem;
  border-radius: 20px;
}

.btn-guide:hover {
  background: #e5e7eb;
  color: #1f2937;
}

.btn-guide svg {
  transition: transform 0.3s ease;
}

.arrow-rotate {
  transform: rotate(180deg);
}

.error-section {
  margin-bottom: 24px;
}

.result-section {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  margin-bottom: 24px;
}

.result-header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.result-header h2 {
  font-size: 1.5rem;
  color: #1f2937;
  margin: 0;
}

.result-time {
  font-size: 0.85rem;
  color: #6b7280;
}

.guide-section {
  text-align: center;
  margin-bottom: 24px;
}

.guide-content {
  background: white;
  border-radius: 20px;
  padding: 24px 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  margin-top: 12px;
  text-align: left;
  color: #374151;
  line-height: 1.7;
}

.guide-block {
  margin-bottom: 20px;
}

.guide-block:last-of-type {
  margin-bottom: 12px;
}

.guide-block h3 {
  font-size: 1.1rem;
  color: #1f2937;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e5e7eb;
}

.guide-block ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.guide-block ul li {
  padding: 6px 0;
  font-size: 0.95rem;
}

.signal-list li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 8px 0;
}

.signal-list li span {
  flex: 1;
}

.guide-disclaimer {
  font-size: 0.8rem;
  color: #9ca3af;
  text-align: center;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}

.footer {
  text-align: center;
  padding: 20px;
  color: #6b7280;
  font-size: 0.9rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .header h1 {
    font-size: 1.8rem;
  }

  .header {
    padding: 30px 16px 20px;
  }

  .subtitle {
    font-size: 0.95rem;
  }

  .main {
    padding: 0 12px 30px;
  }

  .search-section,
  .result-section,
  .guide-content {
    padding: 20px;
    border-radius: 16px;
  }

  .search-box {
    grid-template-columns: 1fr;
  }

  .btn-primary {
    width: 100%;
    justify-content: center;
  }
}
</style>
