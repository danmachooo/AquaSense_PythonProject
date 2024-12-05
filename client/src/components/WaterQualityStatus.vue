<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 transition-all duration-300 hover:shadow-xl">
    <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">Water Quality Status</h3>
    <div class="text-2xl font-bold mb-2" :class="statusColor">
      {{ statusText }}
    </div>
    <p class="text-gray-600 dark:text-gray-400">{{ statusDescription }}</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { API_BASE_URL } from '@/api'

const status = ref()
const statusDescription = ref('')

const statusColor = computed(() => {
  switch (status.value) {
    case "1":
      return 'text-green-500'
    case "0":
      return 'text-red-500'
    default:
      return 'text-gray-500'
  }
})

const statusText = computed(() => {
  switch (status.value) {
    case "1":
      return 'Great'
    case "0":
      return 'Not Great'
    default:
      return 'Cannot classify water quality.'
  }
})

const fetchWaterQualityStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/latest/`, { withCredentials: true })
    status.value = response.data.label
    statusDescription.value = getStatusDescription(status.value)
    console.log('Water quality status fetched:', status.value)
  } catch (error) {
    console.error('Unable to classify water quality:', error)
    status.value = 'Unknown'
    statusDescription.value = 'Unable to fetch water quality status.'
  }
}

const getStatusDescription = (label) => {
  switch (label) {
    case "1":
      return 'The water quality is great for lettuce growth.'
    case "0":
      return 'The water quality is not great for lettuce growth.'
    default:
      return 'Unable to classify water quality.'
  }
}

onMounted(fetchWaterQualityStatus)
</script>

