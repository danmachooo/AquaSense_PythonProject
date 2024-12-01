<template>
  <div>
    <h1 class="text-3xl font-bold mb-8 text-gray-800 dark:text-white">Dashboard</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <MetricCard v-for="metric in metrics" :key="metric.id" :metric="metric" />
    </div>
    <WaterQualityStatus class="mt-8" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import MetricCard from './MetricCard.vue'
import WaterQualityStatus from './WaterQualityStatus.vue'
import { API_BASE_URL } from '@/api'

const metrics = ref([])

const fetchMetrics = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/latest/`, { withCredentials: true })
    const data = response.data
    metrics.value = [
      { id: 1, title: 'Water pH', value: data.pH, unit: '', optimalRange: '6.0 - 7.0', color: 'blue' },
      { id: 2, title: 'Temperature', value: data.temp, unit: '°C', optimalRange: '18°C - 24°C', color: 'red' },
      { id: 3, title: 'Dissolved Oxygen', value: data.DO, unit: 'mg/L', optimalRange: '6 - 9 mg/L', color: 'green' },
      { id: 4, title: 'EC', value: data.EC, unit: 'mS/cm', optimalRange: '1.5 - 2.5 mS/cm', color: 'purple' },
      { id: 5, title: 'Turbidity', value: data.turbidity, unit: 'NTU', optimalRange: '1 - 5 NTU', color: 'yellow' },
      { id: 6, title: 'Nitrogen', value: data.nitrogen, unit: 'ppm', optimalRange: '10 - 20 ppm', color: 'blue' },
      { id: 7, title: 'Phosphorus', value: data.phosphorus, unit: 'ppm', optimalRange: '5 - 8 ppm', color: 'green' },
      { id: 8, title: 'Potassium', value: data.potassium, unit: 'ppm', optimalRange: '100 - 150 ppm', color: 'red' },
      { id: 9, title: 'Hardness', value: data.hardness, unit: 'ppm', optimalRange: '70 - 150 ppm', color: 'purple' }
    ]
  } catch (error) {
    console.error('Error fetching metrics:', error)
  }
}

onMounted(fetchMetrics)
</script>

