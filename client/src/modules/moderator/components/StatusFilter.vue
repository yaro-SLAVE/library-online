<template>
  <div class="filter-group">
    <label class="filter-label">{{ label }}</label>
    <div class="status-checkbox-group">
      <div 
        v-for="status in statusOptions" 
        :key="status.value"
        class="checkbox-item"
      >
        <input
          :id="`status-${status.value}`"
          type="checkbox"
          :value="status.value"
          v-model="localValue"
          :disabled="disabled"
          class="checkbox-input"
        >
        <label :for="`status-${status.value}`" class="checkbox-label">
          {{ status.label }}
        </label>
      </div>
    </div>
    <div v-if="selectedStatuses.length > 0" class="selected-statuses">
      Выбрано: {{ selectedStatuses.join(', ') }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  modelValue: string[];
  label: string;
  disabled?: boolean;
}

interface Emits {
  (e: 'update:modelValue', value: string[]): void;
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false
});

const emit = defineEmits<Emits>();

const localValue = computed({
  get: () => props.modelValue || [],
  set: (value) => emit('update:modelValue', value)
});

const statusOptions = [
  { value: 'new', label: 'Новый' },
  { value: 'processing', label: 'В обработке' },
  { value: 'ready', label: 'Готов к выдаче' },
  { value: 'done', label: 'Выдан' },
  { value: 'cancelled', label: 'Отменен' },
  { value: 'error', label: 'Ошибка' },
  { value: 'archived', label: 'Архивирован' }
];

const selectedStatuses = computed(() => {
  const currentValue = localValue.value || [];
  return currentValue.map(statusValue => {
    const status = statusOptions.find(s => s.value === statusValue);
    return status ? status.label : statusValue;
  });
});
</script>

<style scoped lang="scss">
.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  
  .filter-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--color-text-700);
    margin-bottom: 0.25rem;
  }
}

.status-checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  border: 1px solid var(--color-text-300);
  border-radius: 4px;
  padding: 0.75rem;
  background: white;
  max-height: 8rem;
  overflow-y: auto;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-input {
  margin: 0;
}

.checkbox-label {
  font-size: 0.875rem;
  color: var(--color-text-800);
  cursor: pointer;
  
  &:hover {
    color: var(--color-primary-600);
  }
}

.selected-statuses {
  font-size: 0.75rem;
  color: var(--color-text-600);
  margin-top: 0.25rem;
  font-style: italic;
}
</style>