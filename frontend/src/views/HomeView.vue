<template>
  <div class="app">
    <header class="header">
      <div class="header-inner">
        <h1 class="header-title">趋势信号</h1>
        <p class="header-subtitle">基于 MACD-V 与 RSI 指标的买卖信号研判工具</p>
      </div>
    </header>

    <main class="main">
      <section class="search-card">
        <a-form layout="vertical" class="search-form">
          <a-form-item label="股票列表" class="search-form-item">
            <a-textarea
              v-model:value="inputText"
              placeholder="输入股票名称或代码，支持逗号、空格或换行分隔"
              :rows="3"
              allow-clear
              class="search-textarea"
            />
          </a-form-item>
          <a-form-item class="search-form-action">
            <button
              class="search-btn"
              :disabled="!canQuery || loading"
              @click="handleQuery"
            >
              <svg v-if="loading" class="search-btn-spinner" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" stroke-opacity="0.25" />
                <path d="M12 2a10 10 0 019.95 9" stroke-linecap="round" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8" />
                <path d="M21 21l-4.35-4.35" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              {{ loading ? '查询中...' : '批量查询' }}
            </button>
          </a-form-item>
        </a-form>
      </section>

      <transition name="slide-fade">
        <section v-if="error" class="error-block">
          <a-alert
            :message="error"
            type="error"
            show-icon
            closable
            @close="error = ''"
          />
        </section>
      </transition>

      <transition name="slide-fade">
        <section v-if="result" class="result-card">
          <div class="result-head">
            <div class="result-head-left">
              <h2 class="result-title">查询结果</h2>
            </div>
            <span class="result-time">{{ result.updated_at }}</span>
          </div>
          <IndicatorCards :data="result" />
        </section>
      </transition>

      <section class="guide-section">
        <button class="guide-toggle" @click="guideExpanded = !guideExpanded">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M12 2a10 10 0 100 20 10 10 0 000-20z" />
          </svg>
          <span>使用说明</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" :class="{ 'guide-toggle-arrow-open': guideExpanded }" class="guide-toggle-arrow">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <transition name="slide-fade">
          <div v-if="guideExpanded" class="guide-panel">
            <div class="guide-row">
              <div class="guide-col">
                <h3 class="guide-col-title">指标说明</h3>
                <ul class="guide-list">
                  <li><strong>MACD-V</strong>：衡量价格动量与波动率的比值，反映趋势强度</li>
                  <li><strong>RSI 14</strong>：相对强弱指标，衡量超买超卖状态</li>
                </ul>
              </div>
              <div class="guide-col">
                <h3 class="guide-col-title">交易信号</h3>
                <div class="signal-rows">
                  <div class="signal-row">
                    <a-tag class="signal-tag signal-tag-blue">右侧买点</a-tag>
                    <span class="signal-desc">MACD-V：+50 ~ +150（确认强势），RSI &lt; 30（超卖区）</span>
                  </div>
                  <div class="signal-row">
                    <a-tag class="signal-tag signal-tag-green">左侧买点</a-tag>
                    <span class="signal-desc">MACD-V：&lt; -150（恐慌性超卖），RSI &lt; 30（超卖区）</span>
                  </div>
                  <div class="signal-row">
                    <a-tag class="signal-tag signal-tag-red">左侧卖点</a-tag>
                    <span class="signal-desc">MACD-V：&gt; +150（情绪过热），RSI &gt; 70（超买区）</span>
                  </div>
                  <div class="signal-row">
                    <a-tag class="signal-tag signal-tag-orange">右侧卖点</a-tag>
                    <span class="signal-desc">MACD-V：&lt; +50（趋势转弱），RSI &gt; 70（超买区）</span>
                  </div>
                  <div class="signal-row">
                    <a-tag class="signal-tag signal-tag-gray">观望</a-tag>
                    <span class="signal-desc">MACD-V：-50 ~ +50（无趋势区），无论 RSI 如何都是噪音</span>
                  </div>
                </div>
              </div>
            </div>
            <p class="guide-disclaimer">以上信号仅供参考，不构成投资建议。</p>
          </div>
        </transition>
      </section>
    </main>

    <footer class="footer">
      <p>数据来源：baostock | 仅供参考，不构成投资建议</p>
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
/* ── Root ── */
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  color: #1f2937;
}

/* ── Header ── */
.header {
  border-bottom: 1px solid #eef1f6;
  background: #ffffff;
}
.header-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 28px 20px 18px;
}
.header-title {
  font-size: 1.35rem;
  font-weight: 700;
  color: #1a335e;
  letter-spacing: 0.02em;
  margin: 0 0 4px;
}
.header-subtitle {
  font-size: 0.8rem;
  color: #94a3b8;
  margin: 0;
}

/* ── Main ── */
.main {
  flex: 1;
  max-width: 1100px;
  width: 100%;
  margin: 0 auto;
  padding: 16px 20px 32px;
}

/* ── Search Card ── */
.search-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 18px 20px 4px;
  margin-bottom: 12px;
}
.search-form {
  margin: 0;
}
.search-form :deep(.ant-form-item) {
  margin-bottom: 10px;
}
.search-form-item :deep(.ant-form-item-label > label) {
  font-size: 0.8rem;
  font-weight: 600;
  color: #374151;
}
.search-textarea :deep(.ant-input) {
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 0.875rem;
  background: #fafbfc;
  transition: border-color 0.2s, box-shadow 0.2s;
  resize: vertical;
}
.search-textarea :deep(.ant-input:focus),
.search-textarea :deep(.ant-input-focused) {
  border-color: #274a7e;
  box-shadow: 0 0 0 2px rgba(39, 74, 126, 0.08);
  background: #ffffff;
}
.search-form-action :deep(.ant-form-item-control-input-content) {
  display: flex;
}
.search-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 18px;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  background: #1a335e;
  color: #ffffff;
  height: 34px;
  line-height: 1;
}
.search-btn:hover:not(:disabled) {
  background: #0d1c3e;
  box-shadow: 0 2px 8px rgba(13, 28, 62, 0.2);
}
.search-btn:disabled {
  background: #d1d5db;
  color: #9ca3af;
  cursor: not-allowed;
}
.search-btn-spinner {
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ── Error ── */
.error-block {
  margin-bottom: 12px;
}

/* ── Result Card ── */
.result-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px 20px;
  margin-bottom: 12px;
}
.result-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.result-head-left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.result-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1a335e;
  margin: 0;
}
.result-time {
  font-size: 0.75rem;
  color: #94a3b8;
}

/* ── Guide ── */
.guide-section {
  margin-bottom: 12px;
}
.guide-toggle {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  background: #fafbfc;
  color: #6b7280;
  transition: background 0.2s, color 0.2s, border-color 0.2s;
}
.guide-toggle:hover {
  background: #f3f4f6;
  color: #1a335e;
  border-color: #1a335e;
}
.guide-toggle-arrow {
  transition: transform 0.2s;
}
.guide-toggle-arrow-open {
  transform: rotate(180deg);
}
.guide-panel {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px 20px;
  margin-top: 8px;
  line-height: 1.65;
}
.guide-row {
  display: grid;
  grid-template-columns: 1fr 1.6fr;
  gap: 20px;
}
.guide-col-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1a335e;
  margin: 0 0 8px;
  padding-bottom: 6px;
  border-bottom: 1.5px solid #eef1f6;
}
.guide-list {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 0.8rem;
  color: #4b5563;
}
.guide-list li {
  padding: 3px 0;
}
.signal-rows {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.signal-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  color: #4b5563;
}
.signal-desc {
  flex: 1;
  line-height: 1.5;
}
.signal-tag {
  min-width: 56px;
  text-align: center;
  font-size: 0.72rem;
  padding: 0 6px;
  line-height: 20px;
  border-radius: 3px;
  flex-shrink: 0;
}
.signal-tag-blue {
  background: #e8f0fe;
  color: #1a56db;
  border: 1px solid #c3dafe;
}
.signal-tag-green {
  background: #ecfdf5;
  color: #047857;
  border: 1px solid #a7f3d0;
}
.signal-tag-red {
  background: #fef2f2;
  color: #b91c1c;
  border: 1px solid #fecaca;
}
.signal-tag-orange {
  background: #fff7ed;
  color: #c2410c;
  border: 1px solid #fed7aa;
}
.signal-tag-gray {
  background: #f9fafb;
  color: #6b7280;
  border: 1px solid #e5e7eb;
}
.guide-disclaimer {
  font-size: 0.72rem;
  color: #9ca3af;
  text-align: center;
  margin: 12px 0 0;
  padding-top: 10px;
  border-top: 1px solid #f3f4f6;
}

/* ── Footer ── */
.footer {
  text-align: center;
  padding: 16px 20px;
  color: #9ca3af;
  font-size: 0.78rem;
  border-top: 1px solid #f3f4f6;
}

/* ── Transitions ── */
.slide-fade-enter-active {
  transition: all 0.25s ease-out;
}
.slide-fade-leave-active {
  transition: all 0.15s ease-in;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(-6px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

/* ── Responsive ── */
@media (max-width: 640px) {
  .header-inner {
    padding: 20px 14px 12px;
  }
  .header-title {
    font-size: 1.15rem;
  }
  .main {
    padding: 12px 12px 24px;
  }
  .search-card,
  .result-card {
    padding: 14px;
  }
  .guide-panel {
    padding: 14px;
  }
  .guide-row {
    grid-template-columns: 1fr;
    gap: 14px;
  }
  .search-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
