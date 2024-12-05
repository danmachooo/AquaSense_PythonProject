<template>
  <div class="p-4 sm:p-6 lg:p-8 bg-gray-100 dark:bg-gray-900 min-h-screen">
    <h1 class="text-2xl sm:text-3xl font-bold mb-6 text-gray-800 dark:text-white">Water Quality Reports</h1>

    <!-- Filters and Export -->
    <div class="mb-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="flex items-center space-x-2 w-full sm:w-auto">
          <label for="date-filter" class="text-sm font-medium text-gray-700 dark:text-gray-300">Date Range:</label>
          <select
            id="date-filter"
            v-model="selectedDateRange"
            @change="fetchReports"
            class="rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 dark:bg-gray-700 dark:border-gray-600 dark:text-white w-full sm:w-auto"
          >
            <option value="7">Last 7 days</option>
            <option value="30">Last 30 days</option>
            <option value="90">Last 90 days</option>
          </select>
        </div>
        <div class="flex items-center space-x-2 w-full sm:w-auto">
          <label for="quality-filter" class="text-sm font-medium text-gray-700 dark:text-gray-300">Water Quality:</label>
          <select
            id="quality-filter"
            v-model="selectedQuality"
            class="rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 dark:bg-gray-700 dark:border-gray-600 dark:text-white w-full sm:w-auto"
          >
            <option value="all">All</option>
            <option value="great">Great</option>
            <option value="not-great">Not Great</option>
          </select>
        </div>
        <div class="flex space-x-2 w-full sm:w-auto">
          <button
            @click="openExportModal('excel')"
            class="w-full sm:w-auto px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 transition-colors duration-200"
          >
            <Download class="w-5 h-5 inline-block mr-2" />
            Export to Excel
          </button>
          <button
            @click="openExportModal('pdf')"
            class="w-full sm:w-auto px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 transition-colors duration-200"
          >
            <File class="w-5 h-5 inline-block mr-2" />
            Export to PDF
          </button>
        </div>
      </div>
    </div>

    <!-- Data Table -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700 sticky top-0 z-10">
            <tr>
              <th v-for="column in columns" :key="column.field" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                {{ column.label }}
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="report in paginatedReports" :key="report.id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-150">
              <td v-for="column in columns" :key="column.field" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                <template v-if="column.field === 'timestamp'">
                  {{ formatDate(report[column.field]) }}
                </template>
                <template v-else-if="column.field === 'label'">
                  <span :class="['px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full', getLabelClass(report[column.field])]">
                    {{ report[column.field] === 1 ? 'Great' : 'Not Great' }}
                  </span>
                </template>
                <template v-else>
                  {{ report[column.field] }}
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Pagination -->
    <div class="mt-4 flex items-center justify-between bg-white dark:bg-gray-800 px-4 py-3 rounded-lg shadow-lg">
      <div class="flex-1 flex justify-between sm:hidden">
        <button @click="prevPage" :disabled="currentPage === 1" class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
          Previous
        </button>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
          Next
        </button>
      </div>
      <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
        <div>
          <p class="text-sm text-gray-700 dark:text-gray-300">
            Showing
            <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
            to
            <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, totalItems) }}</span>
            of
            <span class="font-medium">{{ totalItems }}</span>
            results
          </p>
        </div>
        <div>
          <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
            <button @click="prevPage" :disabled="currentPage === 1" class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              <span class="sr-only">Previous</span>
              <ChevronLeft class="h-5 w-5" aria-hidden="true" />
            </button>
            <button @click="nextPage" :disabled="currentPage === totalPages" class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              <span class="sr-only">Next</span>
              <ChevronRight class="h-5 w-5" aria-hidden="true" />
            </button>
          </nav>
        </div>
      </div>
    </div>

    <!-- Export Modal -->
    <div v-if="showExportModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl w-96">
        <h2 class="text-xl font-bold mb-4 text-gray-800 dark:text-white">Export Configuration</h2>
        <div class="mb-4">
          <label for="export-date-range" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Date Range:</label>
          <select
            id="export-date-range"
            v-model="exportDateRange"
            class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          >
            <option value="all">All Data</option>
            <option value="7">Last 7 days</option>
            <option value="30">Last 30 days</option>
            <option value="90">Last 90 days</option>
          </select>
        </div>
        <div class="flex justify-end space-x-2">
          <button @click="closeExportModal" class="px-4 py-2 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-opacity-50 transition-colors duration-200">
            Cancel
          </button>
          <button @click="confirmExport" class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors duration-200">
            Export
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import * as XLSX from 'xlsx'
import { jsPDF } from 'jspdf'
import 'jspdf-autotable'
import { ChevronLeft, ChevronRight, Download, File } from 'lucide-vue-next'

import { API_BASE_URL } from '@/api'

const reports = ref([])
const selectedDateRange = ref('7')
const selectedQuality = ref('all')
const currentPage = ref(1)
const itemsPerPage = 10

const showExportModal = ref(false)
const exportDateRange = ref('all')
const exportType = ref('')

const columns = [
  { label: 'Timestamp', field: 'timestamp' },
  { label: 'pH', field: 'pH' },
  { label: 'Temperature', field: 'temp' },
  { label: 'DO', field: 'DO' },
  { label: 'EC', field: 'EC' },
  { label: 'Turbidity', field: 'turbidity' },
  { label: 'Nitrogen', field: 'nitrogen' },
  { label: 'Phosphorus', field: 'phosphorus' },
  { label: 'Potassium', field: 'potassium' },
  { label: 'Hardness', field: 'hardness' },
  { label: 'Quality', field: 'label' },
]

const filteredReports = computed(() => {
  if (selectedQuality.value === 'all') {
    return reports.value
  } else {
    const qualityValue = selectedQuality.value === 'great' ? 1 : 0
    return reports.value.filter(report => report.label === qualityValue)
  }
})

const totalItems = computed(() => filteredReports.value.length)
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage))

const paginatedReports = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredReports.value.slice(start, end)
})

const fetchReports = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/historical/`, {
      params: { days: selectedDateRange.value }
    })
    reports.value = response.data
    currentPage.value = 1 // Reset to first page when fetching new data
  } catch (error) {
    console.error('Error fetching reports:', error)
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

const getLabelClass = (label) => {
  return label == 1 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
}

const openExportModal = (type) => {
  exportType.value = type
  showExportModal.value = true
}

const closeExportModal = () => {
  showExportModal.value = false
}

const confirmExport = async () => {
  if (exportDateRange.value !== 'all') {
    await fetchReports()
  }
  
  if (exportType.value === 'excel') {
    exportToExcel()
  } else {
    exportToPDF()
  }
  
  closeExportModal()
}

const exportToExcel = () => {
  const worksheet = XLSX.utils.json_to_sheet(filteredReports.value)
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Reports')
  XLSX.writeFile(workbook, `water_quality_reports_${exportDateRange.value}days_${selectedQuality.value}.xlsx`)
}

const exportToPDF = () => {
  const doc = new jsPDF()
  doc.autoTable({
    head: [columns.map(column => column.label)],
    body: filteredReports.value.map(report => 
      columns.map(column => {
        if (column.field === 'label') {
          return report[column.field] === 1 ? 'Great' : 'Not Great'
        }
        if (column.field === 'timestamp') {
          return formatDate(report[column.field])
        }
        return report[column.field]
      })
    ),
  })
  doc.save(`water_quality_reports_${exportDateRange.value}days_${selectedQuality.value}.pdf`)
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

onMounted(() => {
  fetchReports()
})
</script>

<style scoped>
.overflow-x-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.overflow-x-auto::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

@media (max-width: 640px) {
  .overflow-x-auto {
    -webkit-overflow-scrolling: touch;
  }
}
</style>