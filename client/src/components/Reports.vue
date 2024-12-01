<template>
  <div>
    <h1 class="text-3xl font-bold mb-8 text-gray-800 dark:text-white">Reports</h1>
    <div class="mb-4 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center space-x-2">
        <label for="date-filter" class="text-sm font-medium text-gray-700 dark:text-gray-300">Date Range:</label>
        <select
          id="date-filter"
          v-model="selectedDateRange"
          @change="fetchReports"
          class="rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
        >
          <option value="7">Last 7 days</option>
          <option value="30">Last 30 days</option>
          <option value="90">Last 90 days</option>
        </select>
      </div>
      <div class="flex space-x-2">
        <button
          @click="exportToExcel"
          class="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 transition-colors duration-200"
        >
          Export to Excel
        </button>
        <button
          @click="exportToPDF"
          class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 transition-colors duration-200"
        >
          Export to PDF
        </button>
      </div>
    </div>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      <VueGoodTable
        :columns="columns"
        :rows="reports"
        :search-options="{
          enabled: true,
          placeholder: 'Search reports...',
        }"
        :pagination-options="{
          enabled: true,
          mode: 'records',
          perPage: 10,
          position: 'bottom',
          perPageDropdown: [10, 20, 50],
          dropdownAllowAll: false,
          setCurrentPage: 1,
          nextLabel: 'Next',
          prevLabel: 'Prev',
          rowsPerPageLabel: 'Records per page',
          ofLabel: 'of',
          pageLabel: 'page',
          allLabel: 'All',
        }"
        styleClass="vgt-table bordered"
        :sort-options="{
          enabled: true,
          initialSortBy: { field: 'timestamp', type: 'desc' },
        }"
        :table-class="'w-full'"
        :header-class="'bg-gray-50 dark:bg-gray-700'"
        :row-class="'hover:bg-gray-50 dark:hover:bg-gray-700'"
        :cell-class="'px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300'"
      >
        <template #table-column="props">
          <span class="text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">{{ props.column.label }}</span>
        </template>
        <template #table-row="props">
          <span v-if="props.column.field === 'timestamp'">
            {{ formatDate(props.row.timestamp) }}
          </span>
          <span v-else-if="props.column.field === 'label'">
            <span :class="['px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full', getLabelClass(props.row.label)]">
              {{ props.row.label === 1 ? 'Great' : 'Not Great' }}
            </span>
          </span>
          <span v-else>
            {{ props.formattedRow[props.column.field] }}
          </span>
        </template>
      </VueGoodTable>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { VueGoodTable } from 'vue-good-table-next'
import 'vue-good-table-next/dist/vue-good-table-next.css'
import * as XLSX from 'xlsx'
import { jsPDF } from 'jspdf'
import 'jspdf-autotable'
import { API_BASE_URL } from '@/api'

const reports = ref([])
const selectedDateRange = ref('7')

const columns = [
  { label: 'Timestamp', field: 'timestamp', type: 'date', dateInputFormat: 'yyyy-MM-dd\'T\'HH:mm:ss.SSSXXX', dateOutputFormat: 'MM/dd/yyyy HH:mm:ss' },
  { label: 'pH', field: 'pH', type: 'number' },
  { label: 'Temperature', field: 'temp', type: 'number' },
  { label: 'DO', field: 'DO', type: 'number' },
  { label: 'EC', field: 'EC', type: 'number' },
  { label: 'Turbidity', field: 'turbidity', type: 'number' },
  { label: 'Nitrogen', field: 'nitrogen', type: 'number' },
  { label: 'Phosphorus', field: 'phosphorus', type: 'number' },
  { label: 'Potassium', field: 'potassium', type: 'number' },
  { label: 'Hardness', field: 'hardness', type: 'number' },
  { label: 'Quality', field: 'label', type: 'number' },
]

const fetchReports = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/historical/`, { 
      withCredentials: true, 
      params: { days: selectedDateRange.value }
    })
    reports.value = response.data
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

const exportToExcel = () => {
  const worksheet = XLSX.utils.json_to_sheet(reports.value)
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Reports')
  XLSX.writeFile(workbook, 'water_quality_reports.xlsx')
}

const exportToPDF = () => {
  const doc = new jsPDF()
  doc.autoTable({
    head: [columns.map(column => column.label)],
    body: reports.value.map(report => 
      columns.map(column => {
        if (column.field === 'label') {
          return report[column.field] === 1 ? 'Great' : 'Not Great'
        }
        return report[column.field]
      })
    ),
  })
  doc.save('water_quality_reports.pdf')
}

onMounted(fetchReports)
</script>

<style>
.vgt-table.bordered td {
  @apply border-t border-gray-200 dark:border-gray-700;
}
.vgt-table th.line-numbers, .vgt-table th.vgt-checkbox-col {
  @apply bg-gray-50 dark:bg-gray-700;
}
.vgt-table thead th {
  @apply bg-gray-50 dark:bg-gray-700 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider;
}
.vgt-input, .vgt-select {
  @apply bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 rounded-md shadow-sm;
}
.vgt-wrap__footer {
  @apply bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700;
}
.vgt-wrap__footer .footer__navigation__page-btn, .vgt-wrap__footer .footer__navigation__info, .vgt-wrap__footer .footer__navigation__page-info {
  @apply text-gray-700 dark:text-gray-300;
}
.vgt-wrap__footer .footer__navigation__page-btn:hover {
  @apply bg-gray-100 dark:bg-gray-700;
}
</style>

