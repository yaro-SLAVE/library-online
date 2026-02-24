<template>
  <div class="filter-group">
    <label class="filter-label">{{ label }}</label>
    <div class="date-inputs">
      <input 
        v-model="localFrom" 
        type="date" 
        class="filter-input date"
        :disabled="disabled"
        placeholder="От"
      >
      <span class="date-separator">—</span>
      <input 
        v-model="localTo" 
        type="date" 
        class="filter-input date"
        :disabled="disabled"
        placeholder="До"
      >
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  from: string;
  to: string;
  label: string;
  disabled?: boolean;
}

interface Emits {
  (e: 'update:from', value: string): void;
  (e: 'update:to', value: string): void;
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false
});

const emit = defineEmits<Emits>();

const localFrom = computed({
  get: () => props.from,
  set: (value) => emit('update:from', value)
});

const localTo = computed({
  get: () => props.to,
  set: (value) => emit('update:to', value)
});
</script>

<style scoped lang="scss">
.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  .filter-label {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--color-text-700);
    white-space: nowrap;
    text-align: right;
    margin-bottom: 0;
  }
}

.filter-input {
  padding: 0.5rem 0.75rem;
  border: 2px solid var(--color-text-300);
  border-radius: 4px;
  background: white;
  font-size: 0.8rem;
  height: 2.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover:not(:disabled) {
    border-color: var(--color-primary-400);
    cursor: text;
    box-shadow: 0 0 0 1px rgba(var(--color-primary-500-rgb, 59, 130, 246), 0.1);
  }
  
  &:focus {
    outline: none;
    border-color: var(--color-primary-500);
    box-shadow: 0 0 0 2px rgba(var(--color-primary-500-rgb, 59, 130, 246), 0.2);
  }
  
  &:disabled {
    background: var(--color-background-300);
    cursor: not-allowed;
    opacity: 0.6;
    
    &:hover {
      border-color: var(--color-text-300);
      cursor: not-allowed;
    }
  }
}

.date-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-grow: 1;
  
  &:hover .filter-input.date:not(:disabled) {
    border-color: var(--color-primary-400);
  }
}

.date-separator {
  color: var(--color-text-500);
  font-size: 0.8rem;
  font-weight: 500;
  flex-shrink: 0;
  padding: 0 0.125rem;
  transition: color 0.2s ease;
  
  .date-inputs:hover & {
    color: var(--color-primary-500);
  }
}

.filter-input.date {
  flex: 1;
  min-width: 0;
  
  &::-webkit-calendar-picker-indicator {
    cursor: pointer;
    transition: opacity 0.2s ease;
  }
  
  &:hover::-webkit-calendar-picker-indicator {
    opacity: 0.8;
  }
  
  &::placeholder {
    color: var(--color-text-400);
    transition: color 0.2s ease;
  }
  
  &:hover::placeholder {
    color: var(--color-text-500);
  }
}
</style>