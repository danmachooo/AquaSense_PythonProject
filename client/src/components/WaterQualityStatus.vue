<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 transition-all duration-300 hover:shadow-xl">
    <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">Water Quality Status</h3>
    <div class="text-2xl font-bold mb-2" :class="statusColor">
      {{ status }}
    </div>
    <p class="text-gray-600 dark:text-gray-400">{{ statusDescription }}</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { API_BASE_URL } from '@/api'

const status = ref('')
const statusDescription = ref('')

const statusColor = computed(() => {
  switch (status.value) {
    case 'Excellent':
      return 'text-green-500'
    case 'Good':
      return 'text-blue-500'
    case 'Fair':
      return 'text-yellow-500'
    case 'Poor':
      return 'text-red-500'
    default:
      return 'text-gray-500'
  }
})

const fetchWaterQualityStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/latest/`, { withCredentials: true })
    status.value = response.data.water_quality_label
    statusDescription.value = getStatusDescription(status.value)
  } catch (error) {
    console.error('Error fetching water quality status:', error)
    status.value = 'Unknown'
    statusDescription.value = 'Unable to fetch water quality status.'
  }
}

const getStatusDescription = (status) => {
  switch (status) {
    case 'Excellent':
      return 'All parameters are within optimal ranges for lettuce growth.'
    case 'Good':
      return 'Most parameters are within optimal ranges. Minor adjustments may be needed.'
    case 'Fair':
      return 'Some parameters are outside optimal ranges. Attention is required.'
    case 'Poor':
      return 'Multiple parameters are outside optimal ranges. Immediate action is needed.'
    default:
      return 'Unable to determine water quality status.'
  }
}

onMounted(fetchWaterQualityStatus)
</script>

