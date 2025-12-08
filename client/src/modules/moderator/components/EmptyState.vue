<template>
  <div class="empty-state">
    <div class="empty-state-content">
      <p v-if="hasActiveFilters">Нет читателей, соответствующих фильтрам</p>
      <p v-else>Нет данных о читателях</p>
      
      <button 
        v-if="hasActiveFilters"
        @click="$emit('clear-filters')" 
        class="clear-filters-btn"
        type="button"
        :disabled="loading"
      >
        Сбросить фильтры
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  hasActiveFilters: boolean;
  loading: boolean;
}

interface Emits {
  (e: 'clear-filters'): void;
}

defineProps<Props>();
defineEmits<Emits>();
</script>

<style scoped lang="scss">
.empty-state {
  padding: 3rem;
  text-align: center;
  color: var(--color-text-600);
}

.empty-state-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

.clear-filters-btn {
  background: var(--color-primary-500);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  
  &:hover:not(:disabled) {
    background: var(--color-primary-600);
  }
  
  &:disabled {
    background: var(--color-text-300);
    cursor: not-allowed;
    opacity: 0.6;
  }
}
</style>