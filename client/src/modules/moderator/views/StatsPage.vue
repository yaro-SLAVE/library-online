<!-- StatsPage.vue -->
<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useStatsStore } from "../store/stats";
import LiveStatsBlock from "../components/LiveStatsBlock.vue";
import ExcelExportPanel from "../components/ExcelExportPanel.vue";
import type { LiveStats } from "@core/api/types";
const statsStore = useStatsStore();
const stats = ref<LiveStats>();
const isLoading = ref(true);

const handleExport = async (selectedColumns: string[]) => {
  //     await statsStore.exportToExcel(selectedColumns);
};

onMounted(async () => {
  try {
    stats.value = await statsStore.getLiveStats();
  } catch (error) {
    console.error("Failed to load stats:", error);
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <div>
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Статистика библиотеки</h1>
        <p class="page-subtitle">Мониторинг заказов и аналитика работы</p>
      </div>
    </div>

    <div class="page-content">
      <section class="stats-section">
        <div class="section-header">
          <h2 class="section-title">Текущая статистика</h2>
          <div class="section-actions"></div>
        </div>

        <div class="stats-content">
          <LiveStatsBlock v-if="stats && !isLoading" :="stats" />
          <div v-else-if="isLoading" class="loading-state">
            <div class="loading-spinner"></div>
            <span>Загрузка статистики...</span>
          </div>
          <div v-else class="error-state">
            <p>Не удалось загрузить статистику</p>
            <button class="retry-btn" @click="$router.go(0)">Попробовать снова</button>
          </div>
        </div>
      </section>

      <ExcelExportPanel @export="handleExport" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-header {
  color: var(--color-primary-700);
  padding: 3rem 2rem;

  .header-content {
    max-width: 1200px;
    margin: 0 auto;
    text-align: center;
  }

  .page-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
  }

  .page-subtitle {
    font-size: 1.2rem;
    margin: 0;
    opacity: 0.9;
    font-weight: 400;
  }
}

.page-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.stats-section,
.export-section {
  background: var(--color-background-100);
  border-radius: 20px;
  border: 1px solid var(--color-background-200);
  box-shadow: 0 4px 12px rgba(102, 69, 186, 0.1);
  overflow: hidden;
}

.section-header {
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid var(--color-background-200);

  .section-title {
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--color-primary-700);
    margin: 0 0 0.5rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;

    &::before {
      content: "";
      width: 4px;
      height: 24px;
      background: var(--color-primary-500);
      border-radius: 2px;
    }
  }

  .section-description {
    color: var(--color-text-600);
    margin: 0;
    font-size: 1rem;
  }
}

.stats-section .section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.section-actions {
  display: flex;
  gap: 1rem;
}

.refresh-btn {
  background: var(--color-primary-500);
  color: var(--color-text-50);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 69, 186, 0.3);

  &:hover {
    background: var(--color-primary-600);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 69, 186, 0.4);
  }

  &:active {
    transform: translateY(0);
  }
}

.stats-content {
  padding: 2rem;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  gap: 1rem;
  text-align: center;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid var(--color-primary-100);
  border-top: 3px solid var(--color-primary-500);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-state {
  color: var(--color-accent-600);

  p {
    margin: 0 0 1rem 0;
    font-size: 1.1rem;
  }
}

.retry-btn {
  background: var(--color-accent-500);
  color: var(--color-text-50);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: var(--color-accent-600);
  }
}

.export-content {
  padding: 2rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 2rem 1rem;

    .page-title {
      font-size: 2rem;
    }

    .page-subtitle {
      font-size: 1rem;
    }
  }

  .page-content {
    padding: 1rem;
    gap: 2rem;
  }

  .stats-section .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .section-actions {
    justify-content: center;
  }

  .stats-content,
  .export-content {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .page-header {
    padding: 1.5rem 1rem;

    .page-title {
      font-size: 1.75rem;
    }
  }

  .section-header {
    padding: 1.5rem 1.5rem 1rem;

    .section-title {
      font-size: 1.5rem;
    }
  }
}
</style>
