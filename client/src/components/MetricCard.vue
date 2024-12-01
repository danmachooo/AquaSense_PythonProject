<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 transition-all duration-300 hover:shadow-xl">
    <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">{{ metric.title }}</h3>
    <div class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
      {{ metric.value }}{{ metric.unit }}
    </div>
    <div class="text-sm text-gray-500 dark:text-gray-400 mb-4">
      Optimal range: {{ metric.optimalRange }}
    </div>
    <div class="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
      <div
        class="h-full rounded-full transition-all duration-300 ease-in-out"
        :class="`bg-${metric.color}-500`"
        :style="{ width: `${calculatePercentage(metric.value, metric.optimalRange)}%` }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'

const props = defineProps({
  metric: {
    type: Object,
    required: true
  }
})

const calculatePercentage = (value, range) => {
  const [min, max] = range.split(' - ').map(parseFloat)
  const percentage = ((value - min) / (max - min)) * 100
  return Math.min(Math.max(percentage, 0), 100)
}

const statusColor = computed(() => {
  const percentage = calculatePercentage(props.metric.value, props.metric.optimalRange)
  if (percentage < 25 || percentage > 75) return 'bg-red-500'
  if (percentage < 40 || percentage > 60) return 'bg-yellow-500'
  return 'bg-green-500'
})
</script>

