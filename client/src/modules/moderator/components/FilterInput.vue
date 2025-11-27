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
  flex-direction: column;
  gap: 0.25rem;
  
  .filter-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--color-text-700);
    margin-bottom: 0.25rem;
  }
}

.filter-input {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-text-300);
  border-radius: 4px;
  background: white;
  font-size: 0.875rem;
  height: 2.25rem;
  
  &:focus {
    outline: none;
    border-color: var(--color-primary-500);
  }
  
  &:disabled {
    background: var(--color-background-300);
    cursor: not-allowed;
    opacity: 0.6;
  }
}
</style>