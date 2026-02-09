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

.date-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.date-separator {
  color: var(--color-text-500);
  font-size: 0.875rem;
  font-weight: 500;
  flex-shrink: 0;
}
</style>