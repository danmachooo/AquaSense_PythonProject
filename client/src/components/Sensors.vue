<template>
  <div>
    <h1 class="text-3xl font-bold mb-8 text-gray-800 dark:text-white">Sensors</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="sensor in sensors" :key="sensor.name" class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 transition-all duration-300 hover:shadow-xl">
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">{{ sensor.name }}</h3>
        <div class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          {{ sensor.value }}{{ sensor.unit }}
        </div>
        <span :class="['px-2 py-1 rounded-full text-sm', sensor.status === 'Normal' ? 'bg-green-200 text-green-800' : 'bg-yellow-200 text-yellow-800']">
          {{ sensor.status }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { API_BASE_URL } from '@/api'

const sensors = ref([])

const fetchSensors = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/latest/`, { withCredentials: true })
    const data = response.data
    sensors.value = [
      { name: 'Main Tank pH', value: data.pH, unit: '', status: getStatus(data.pH, 6.0, 7.0) },
      { name: 'Nutrient Solution Temp', value: data.temp, unit: '°C', status: getStatus(data.temp, 18, 24) },
      { name: 'Dissolved Oxygen', value: data.DO, unit: 'mg/L', status: getStatus(data.DO, 6, 8) },
      { name: 'EC Sensor', value: data.EC, unit: 'mS/cm', status: getStatus(data.EC, 1.2, 1.8) },
      { name: 'Turbidity', value: data.turbidity, unit: 'NTU', status: getStatus(data.turbidity, 0, 5) },
      { name: 'Nitrogen', value: data.nitrogen, unit: 'ppm', status: getStatus(data.nitrogen, 100, 200) },
      { name: 'Phosphorus', value: data.phosphorus, unit: 'ppm', status: getStatus(data.phosphorus, 30, 50) },
      { name: 'Potassium', value: data.potassium, unit: 'ppm', status: getStatus(data.potassium, 150, 300) },
      { name: 'Hardness', value: data.hardness, unit: 'ppm', status: getStatus(data.hardness, 100, 200) }
    ]
  } catch (error) {
    console.error('Error fetching sensors:', error)
  }
}

const getStatus = (value, min, max) => {
  return (value >= min && value <= max) ? 'Normal' : 'Attention'
}

onMounted(fetchSensors)
</script>

