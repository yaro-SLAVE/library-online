<template>
  <div class="date-filter">
    <div class="filter-row">
      <div class="date-input-group">
        <label class="date-label">Дата от:</label>
        <input
          v-model="startDate"
          type="date"
          class="date-input"
          @change="handleDateChange"
        />
      </div>
      
      <div class="date-input-group">
        <label class="date-label">до:</label>
        <input
          v-model="endDate"
          type="date"
          class="date-input"
          @change="handleDateChange"
        />
      </div>
      
      <button 
        class="search-button"
        @click="handleSearch"
        :disabled="!isFormValid || loading"
      >
        <span v-if="loading">Поиск...</span>
        <span v-else>Найти</span>
      </button>
    </div>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";

const props = defineProps<{
  loading: boolean;
}>();

const emit = defineEmits<{
  (e: "search", startDate: string, endDate: string): void;
  (e: "initialDates", startDate: string, endDate: string): void; // Новый emit
}>();

const startDate = ref('');
const endDate = ref('');
const error = ref('');

// Валидация формы
const isFormValid = computed(() => {
  return startDate.value && endDate.value;
});

// Установка дат по умолчанию (последние 30 дней)
const setDefaultDates = () => {
  const end = new Date();
  const start = new Date();
  start.setDate(start.getDate() - 30);
  
  endDate.value = end.toISOString().split('T')[0];
  startDate.value = start.toISOString().split('T')[0];
  
  // Эмитим начальные даты
  emit("initialDates", startDate.value, endDate.value);
};

const handleDateChange = () => {
  error.value = '';
  
  // Проверка что начальная дата не больше конечной
  if (startDate.value && endDate.value && startDate.value > endDate.value) {
    error.value = 'Начальная дата не может быть больше конечной';
  }
};

const handleSearch = () => {
  if (!isFormValid.value) {
    error.value = 'Заполните обе даты';
    return;
  }
  
  if (startDate.value > endDate.value) {
    error.value = 'Начальная дата не может быть больше конечной';
    return;
  }
  
  error.value = '';
  emit("search", startDate.value, endDate.value);
};

onMounted(() => {
  setDefaultDates();
});
</script>

<style scoped lang="scss">
.date-filter {
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  align-items: end;
  gap: 16px;
  flex-wrap: wrap;
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
}

.date-input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.date-label {
  font-size: 0.9em;
  color: var(--color-text-600);
  font-weight: 500;
}

.date-input {
  padding: 8px 12px;
  border: 1px solid var(--color-text-200);
  border-radius: 6px;
  font-size: 14px;
  background-color: var(--color-background-100);
  color: var(--color-text-800);
  transition: border-color 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: var(--color-primary-400);
  }
  
  &:invalid {
    border-color: var(--color-accent-400);
  }
}

.search-button {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  background-color: var(--color-primary-400);
  color: var(--color-text-50);
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  height: fit-content;
  
  &:hover:not(:disabled) {
    background-color: var(--color-primary-500);
  }
  
  &:disabled {
    background-color: var(--color-text-400);
    cursor: not-allowed;
    opacity: 0.7;
  }
  
  @media (max-width: 768px) {
    align-self: flex-start;
  }
}

.error-message {
  color: var(--color-accent-400);
  font-size: 0.9em;
  margin-top: 8px;
  padding: 8px 12px;
  background-color: var(--color-accent-50);
  border-radius: 4px;
  border-left: 3px solid var(--color-accent-400);
}
</style>