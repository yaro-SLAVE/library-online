<template>
  <div class="filter-group">
    <label :for="id" class="filter-label">{{ label }}</label>
    <input 
      :id="id"
      v-model="localValue" 
      type="text" 
      :placeholder="placeholder"
      class="filter-input"
      :disabled="disabled"
    >
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  modelValue: string;
  label: string;
  placeholder?: string;
  disabled?: boolean;
  id?: string;
}

interface Emits {
  (e: 'update:modelValue', value: string): void;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '',
  disabled: false,
  id: undefined
});

const emit = defineEmits<Emits>();

const localValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
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
    cursor: pointer;
    
    &:hover {
      color: var(--color-primary-600);
    }
  }
}

.filter-input {
  padding: 0.5rem 0.75rem;
  border: 2px solid var(--color-text-300);
  border-radius: 4px;
  background: white;
  font-size: 0.8rem;
  height: 2.25rem;
  flex-grow: 1;
  transition: all 0.2s ease;

  &:hover:not(:disabled) {
    border-color: var(--color-primary-400);
    box-shadow: 0 0 0 1px rgba(var(--color-primary-500-rgb, 59, 130, 246), 0.1);
  }
  
  &:focus {
    outline: none;
    border-color: var(--color-primary-500);
    box-shadow: 0 0 0 2px rgba(var(--color-primary-500-rgb, 59, 130, 246), 0.2);
  }
    
  &:disabled {
    background: var(--color-background-300);
    opacity: 0.6;
    
    &:hover {
      border-color: var(--color-text-300);
    }
    
    &:focus {
      border-color: var(--color-primary-500);
    }
    
    &:disabled {
      background: var(--color-background-300);
      opacity: 0.6;
    }
  }
}
</style>