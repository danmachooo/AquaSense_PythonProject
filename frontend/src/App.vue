<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <div class="flex">
      <!-- Sidebar -->
      <aside class="w-64 bg-white dark:bg-gray-800 min-h-screen">
        <div class="p-4">
          <h1 class="text-2xl font-bold text-green-600 dark:text-green-400">Water Monitor</h1>
          <nav class="mt-8">
            <router-link to="/" class="block py-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">Dashboard</router-link>
            <router-link to="/sensors" class="block py-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">Sensors</router-link>
            <router-link to="/reports" class="block py-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">Reports</router-link>
          </nav>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 p-8">
        <router-view></router-view>
      </main>
    </div>

    <!-- Theme Toggle Button -->
    <button @click="toggleTheme" class="fixed bottom-8 left-8 px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-gray-700 dark:text-gray-300">
      Toggle Dark Mode
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const isDark = ref(false)

const toggleTheme = () => {
  isDark.value = !isDark.value
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  applyTheme()
}

const applyTheme = () => {
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  isDark.value = savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)
  applyTheme()
})

watch(isDark, applyTheme)
</script>

<style>

</style>