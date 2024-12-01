<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 transition-colors duration-300">
    <div class="flex">
      <!-- Sidebar -->
      <aside class="w-64 bg-white dark:bg-gray-800 min-h-screen shadow-lg transition-colors duration-300">
        <div class="p-4">
          <h1 class="text-2xl font-bold text-green-600 dark:text-green-400">Water Monitor</h1>
          <nav class="mt-8 space-y-2">
            <router-link 
              v-for="link in navLinks" 
              :key="link.to" 
              :to="link.to" 
              class="block px-4 py-2 rounded-md transition-colors duration-200"
              :class="[$route.path === link.to ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-100' : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700']"
            >
              <component :is="link.icon" class="inline-block w-5 h-5 mr-2" />
              {{ link.text }}
            </router-link>
          </nav>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 p-8 overflow-auto">
        <div class="max-w-7xl mx-auto">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>
    </div>

    <!-- Theme Toggle Button -->
    <button 
      @click="toggleTheme" 
      class="fixed bottom-8 right-8 p-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-full shadow-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
      aria-label="Toggle Dark Mode"
    >
      <SunIcon v-if="isDark" class="w-6 h-6 text-yellow-400" />
      <MoonIcon v-else class="w-6 h-6 text-gray-700" />
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { SunIcon, MoonIcon, HomeIcon, ChartBarIcon, DocumentReportIcon } from '@heroicons/vue/outline'

const route = useRoute()
const isDark = ref(false)

const navLinks = [
  { to: '/', text: 'Dashboard', icon: HomeIcon },
  { to: '/sensors', text: 'Sensors', icon: ChartBarIcon },
  { to: '/reports', text: 'Reports', icon: DocumentReportIcon },
]

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
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>