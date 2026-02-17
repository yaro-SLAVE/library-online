<template>
  <div>
    <div v-if="dateError" class="error-message">
      {{ dateError }}
    </div>

    <div class="filters-section">
      <div class="filters-grid">
        <FilterInput
          v-model="localFilters.fullname"
          label="ФИО читателя"
          placeholder="Поиск по ФИО..."
          :disabled="loading"
          id="fullname-filter"
        />

        <FilterInput
          v-model="localFilters.libraryName"
          label="Библиотека"
          placeholder="Поиск по библиотеке..."
          :disabled="loading"
          id="library-filter"
        />

        <button 
          @click="$emit('apply-filters', localFilters)" 
          class="apply-filters-btn"
          type="button"
          :disabled="loading || !hasFilterChanges"
        >
          Применить
        </button>

        <FilterInput
          v-model="localFilters.employeeCollect"
          label="Сотрудник-сборщик"
          placeholder="Кто собирал..."
          :disabled="loading"
          id="employee-collect-filter"
        />

        <FilterInput
          v-model="localFilters.employeeIssue"
          label="Сотрудник-выдающий"
          placeholder="Кто выдавал..."
          :disabled="loading"
          id="employee-issue-filter"
        />

        <button 
          v-if="hasActiveFilters"
          @click="$emit('clear-filters')" 
          class="clear-filters-btn"
          type="button"
          :disabled="loading"
        >
          Сбросить
        </button>

        <StatusFilter
          v-model="localFilters.statuses"
          label="Статусы заказов"
          :disabled="loading"
        />

        <DateRangeFilter
          v-model:from="localFilters.dateFrom"
          v-model:to="localFilters.dateTo"
          label="Дата создания"
          :disabled="loading"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import FilterInput from '@modules/moderator/components/FilterInput.vue';
import DateRangeFilter from '@modules/moderator/components/DateRangeFilter.vue';
import StatusFilter from '@modules/moderator/components/StatusFilter.vue';

interface Props {
  filters: any;
  loading: boolean;
  dateError?: string;
  hasActiveFilters: boolean;
  hasFilterChanges: boolean;
}

interface Emits {
  (e: 'apply-filters', filters: any): void;
  (e: 'clear-filters'): void;
  (e: 'update:filters', filters: any): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const localFilters = computed({
  get: () => props.filters,
  set: (value) => emit('update:filters', value)
});
</script>

<style scoped lang="scss">
.filters-section {
  background: var(--color-background-200);
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  border: 1px solid var(--color-text-200);
}

.filters-grid {
  display: grid;
  grid-template-columns: 2fr 2fr 1fr;
  gap: 1rem;
  align-items: end;
}

.apply-filters-btn,
.clear-filters-btn {
  align-self: center;
  background: var(--color-primary-500);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  height: fit-content;
  
  &:hover:not(:disabled) {
    background: var(--color-primary-600);
  }
  
  &:disabled {
    background: var(--color-text-300);
    cursor: not-allowed;
    opacity: 0.6;
  }
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  border: 1px solid #fcc;
  font-size: 0.875rem;
}
</style>