<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 transition-colors duration-300">
    <div class="flex flex-col md:flex-row">
      <!-- Sidebar -->
      <aside 
        :class="[
          'bg-white dark:bg-gray-800 shadow-lg transition-all duration-300',
          isSidebarOpen ? 'w-64' : 'w-0 md:w-16',
          'fixed md:sticky top-0 left-0 z-30 h-screen overflow-y-auto'
        ]"
      >
        <div class="p-4">
          <div class="flex flex-col items-center justify-center mb-8">
            <h1 
              :class="[
              'text-2xl font-bold text-green-600 dark:text-green-400 transition-all duration-300 text-center',
              isSidebarOpen ? 'opacity-100 mb-2' : 'opacity-0 md:opacity-100 md:mb-0'
            ]"
            >
              <span class="hidden md:inline">AquaSense</span>
              <span class="md:hidden">AS</span>
            </h1>
            <button 
              @click="toggleSidebar" 
              class="md:hidden text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            >
              <MenuIcon v-if="!isSidebarOpen" class="w-6 h-6" />
              <XIcon v-else class="w-6 h-6" />
            </button>
          </div>
          <nav class="mt-8 space-y-2">
            <router-link 
              v-for="link in navLinks" 
              :key="link.to" 
              :to="link.to" 
              class="flex items-center px-4 py-2 rounded-md transition-colors duration-200"
              :class="[$route.path === link.to ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-100' : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700']"
            >
              <component :is="link.icon" class="w-5 h-5" />
              <span 
                :class="[
                  'ml-2 transition-opacity duration-300',
                  isSidebarOpen ? 'opacity-100' : 'opacity-0 md:opacity-100'
                ]"
              >
                {{ link.text }}
              </span>
            </router-link>
          </nav>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 p-4 md:p-8 overflow-auto">
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
      class="fixed bottom-4 right-4 md:bottom-8 md:right-8 p-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-full shadow-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
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
import { SunIcon, MoonIcon, HomeIcon, ChartBarIcon, DocumentReportIcon, MenuIcon, XIcon } from 'lucide-vue-next'

const route = useRoute()
const isDark = ref(false)
const isSidebarOpen = ref(window.innerWidth >= 768)

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

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
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

  window.addEventListener('resize', () => {
    if (window.innerWidth >= 768) {
      isSidebarOpen.value = true
    }
  })
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