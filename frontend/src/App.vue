<template>
  <n-config-provider :locale="zhCN" :date-locale="dateZhCN">
    <n-message-provider>
      <HomeView />
    </n-message-provider>
  </n-config-provider>
</template>

<script setup>
import { NConfigProvider, NMessageProvider, zhCN, dateZhCN } from 'naive-ui'
import HomeView from './views/HomeView.vue'
</script>
