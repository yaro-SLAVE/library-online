<template>
  <div class="pagination">
    <button 
      @click="$emit('prev')" 
      :disabled="currentPage === 1 || loading"
      class="pagination-btn"
      type="button"
      aria-label="Предыдущая страница"
    >
      Назад
    </button>
    <span class="pagination-info">
      Страница {{ currentPage }} из {{ totalPages }}
    </span>
    <button 
      @click="$emit('next')" 
      :disabled="currentPage >= totalPages || loading"
      class="pagination-btn"
      type="button"
      aria-label="Следующая страница"
    >
      Вперед
    </button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  currentPage: number;
  totalPages: number;
  loading: boolean;
}

interface Emits {
  (e: 'prev'): void;
  (e: 'next'): void;
}

defineProps<Props>();
defineEmits<Emits>();
</script>

<style scoped lang="scss">
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
  padding: 1rem;
}

.pagination-btn {
  background: var(--color-primary-500);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  
  &:hover:not(:disabled) {
    background: var(--color-primary-600);
  }
  
  &:disabled {
    background: var(--color-text-300);
    cursor: not-allowed;
    opacity: 0.6;
  }
}

.pagination-info {
  color: var(--color-text-600);
  font-size: 0.875rem;
}
</style>