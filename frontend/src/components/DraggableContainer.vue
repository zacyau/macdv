<template>
  <div
    ref="containerRef"
    class="draggable-wrapper"
    @touchstart="onTouchStart"
    @touchmove="onTouchMove"
    @touchend="onTouchEnd"
    @mousedown="onMouseDown"
  >
    <div
      ref="contentRef"
      class="draggable-content"
      :style="contentStyle"
    >
      <slot />
    </div>
    <div v-if="showHIndicator" class="scroll-indicator scroll-indicator-h">
      <div class="scroll-indicator-line" />
    </div>
    <div v-if="showVIndicator" class="scroll-indicator scroll-indicator-v">
      <div class="scroll-indicator-line" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const containerRef = ref(null)
const contentRef = ref(null)

const translateX = ref(0)
const translateY = ref(0)
const isDragging = ref(false)
const startX = ref(0)
const startY = ref(0)
const startTranslateX = ref(0)
const startTranslateY = ref(0)
const velocityX = ref(0)
const velocityY = ref(0)
const lastX = ref(0)
const lastY = ref(0)
const lastTime = ref(0)
const rafId = ref(null)

const contentStyle = computed(() => ({
  transform: `translate3d(${translateX.value}px, ${translateY.value}px, 0)`,
  willChange: isDragging.value ? 'transform' : 'auto',
}))

const showHIndicator = ref(false)
const showVIndicator = ref(false)

function updateIndicators() {
  if (!containerRef.value || !contentRef.value) return
  const cw = containerRef.value.clientWidth
  const ch = containerRef.value.clientHeight
  const bw = contentRef.value.scrollWidth
  const bh = contentRef.value.scrollHeight
  showHIndicator.value = bw > cw + 4
  showVIndicator.value = bh > ch + 4
}

function getClientPos(e) {
  if (e.touches && e.touches.length) {
    return { x: e.touches[0].clientX, y: e.touches[0].clientY }
  }
  return { x: e.clientX, y: e.clientY }
}

function clamp(val, min, max) {
  return Math.max(min, Math.min(max, val))
}

function computeBounds() {
  if (!containerRef.value || !contentRef.value) return { minX: 0, maxX: 0, minY: 0, maxY: 0 }
  const cw = containerRef.value.clientWidth
  const ch = containerRef.value.clientHeight
  const bw = contentRef.value.scrollWidth
  const bh = contentRef.value.scrollHeight
  return {
    minX: Math.min(0, cw - bw),
    maxX: 0,
    minY: Math.min(0, ch - bh),
    maxY: 0,
  }
}

function onTouchStart(e) {
  if (e.touches.length !== 1) return
  const pos = getClientPos(e)
  startDrag(pos.x, pos.y)
}

function onMouseDown(e) {
  const pos = getClientPos(e)
  startDrag(pos.x, pos.y)
  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
}

function startDrag(x, y) {
  isDragging.value = true
  startX.value = x
  startY.value = y
  startTranslateX.value = translateX.value
  startTranslateY.value = translateY.value
  lastX.value = x
  lastY.value = y
  lastTime.value = performance.now()
  velocityX.value = 0
  velocityY.value = 0
  cancelAnimationFrame(rafId.value)
}

function onTouchMove(e) {
  if (!isDragging.value) return
  e.preventDefault()
  const pos = getClientPos(e)
  doDrag(pos.x, pos.y)
}

function onMouseMove(e) {
  if (!isDragging.value) return
  e.preventDefault()
  const pos = getClientPos(e)
  doDrag(pos.x, pos.y)
}

function doDrag(x, y) {
  const now = performance.now()
  const dt = now - lastTime.value
  if (dt > 0) {
    velocityX.value = (x - lastX.value) / dt
    velocityY.value = (y - lastY.value) / dt
  }
  lastX.value = x
  lastY.value = y
  lastTime.value = now

  const dx = x - startX.value
  const dy = y - startY.value
  const bounds = computeBounds()

  translateX.value = clamp(startTranslateX.value + dx, bounds.minX - 40, bounds.maxX + 40)
  translateY.value = clamp(startTranslateY.value + dy, bounds.minY - 40, bounds.maxY + 40)
}

function onTouchEnd() {
  endDrag()
}

function onMouseUp() {
  endDrag()
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', onMouseUp)
}

function endDrag() {
  if (!isDragging.value) return
  isDragging.value = false
  const bounds = computeBounds()
  let targetX = clamp(translateX.value, bounds.minX, bounds.maxX)
  let targetY = clamp(translateY.value, bounds.minY, bounds.maxY)

  const vx = velocityX.value * 16
  const vy = velocityY.value * 16
  if (Math.abs(vx) > 2 || Math.abs(vy) > 2) {
    targetX = clamp(translateX.value + vx * 15, bounds.minX, bounds.maxX)
    targetY = clamp(translateY.value + vy * 15, bounds.minY, bounds.maxY)
  }

  animateTo(targetX, targetY)
}

function animateTo(targetX, targetY) {
  const startXVal = translateX.value
  const startYVal = translateY.value
  const start = performance.now()
  const duration = 350

  function step(now) {
    const t = Math.min((now - start) / duration, 1)
    const ease = 1 - Math.pow(1 - t, 3)
    translateX.value = startXVal + (targetX - startXVal) * ease
    translateY.value = startYVal + (targetY - startYVal) * ease
    if (t < 1) {
      rafId.value = requestAnimationFrame(step)
    }
  }
  rafId.value = requestAnimationFrame(step)
}

let ro = null
onMounted(() => {
  updateIndicators()
  ro = new ResizeObserver(updateIndicators)
  if (containerRef.value) ro.observe(containerRef.value)
  if (contentRef.value) ro.observe(contentRef.value)
})

onUnmounted(() => {
  cancelAnimationFrame(rafId.value)
  if (ro) ro.disconnect()
})
</script>

<style scoped>
.draggable-wrapper {
  position: relative;
  overflow: hidden;
  touch-action: none;
  -webkit-user-select: none;
  user-select: none;
}

.draggable-content {
  display: inline-block;
  min-width: 100%;
}

.scroll-indicator {
  position: absolute;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.draggable-wrapper:hover .scroll-indicator,
.draggable-wrapper:active .scroll-indicator {
  opacity: 1;
}

.scroll-indicator-h {
  bottom: 4px;
  left: 50%;
  transform: translateX(-50%);
}

.scroll-indicator-h .scroll-indicator-line {
  width: 36px;
  height: 3px;
  border-radius: 2px;
  background: rgba(26, 51, 94, 0.18);
}

.scroll-indicator-v {
  right: 4px;
  top: 50%;
  transform: translateY(-50%);
}

.scroll-indicator-v .scroll-indicator-line {
  width: 3px;
  height: 36px;
  border-radius: 2px;
  background: rgba(26, 51, 94, 0.18);
}
</style>
