<template>
  <div class="filter-group">
    <label class="filter-label">{{ label }}</label>
    <div class="status-filter-container">
      <button 
        type="button"
        class="status-filter-toggle"
        @click="toggleDropdown"
        :disabled="disabled"
      >
        <span v-if="selectedCount === 0">Все статусы</span>
        <span v-else>Выбрано: {{ selectedCount }}</span>
        <span class="arrow" :class="{ open: isOpen }">▼</span>
      </button>
      
      <div v-if="isOpen" class="status-dropdown" @click.stop>
        <div class="status-options">
          <label 
            v-for="status in availableStatuses" 
            :key="status.value"
            class="status-option"
          >
            <input
              type="checkbox"
              :value="status.value"
              :checked="isSelected(status.value)"
              @change="toggleStatus(status.value)"
            />
            <span class="status-badge" :class="`status-${status.value}`">
              {{ status.label }}
            </span>
          </label>
        </div>
        
        <div class="dropdown-footer">
          <button 
            type="button"
            class="clear-btn"
            @click="clearSelection"
          >
            Очистить
          </button>
          <button 
            type="button"
            class="select-all-btn"
            @click="selectAll"
          >
            Выбрать все
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import type { OrderStatusEnum } from '@api/types';
import { orderStatuses } from '@api/types';

interface Props {
  modelValue: OrderStatusEnum[];
  label: string;
  disabled?: boolean;
}

interface Emits {
  (e: 'update:modelValue', value: OrderStatusEnum[]): void;
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false
});

const emit = defineEmits<Emits>();

const isOpen = ref(false);

const availableStatuses = [
  { value: 'new' as OrderStatusEnum, label: orderStatuses.new },
  { value: 'processing' as OrderStatusEnum, label: orderStatuses.processing },
  { value: 'ready' as OrderStatusEnum, label: orderStatuses.ready },
  { value: 'done' as OrderStatusEnum, label: orderStatuses.done },
  { value: 'cancelled' as OrderStatusEnum, label: orderStatuses.cancelled },
  { value: 'error' as OrderStatusEnum, label: orderStatuses.error },
  { value: 'archived' as OrderStatusEnum, label: orderStatuses.archived },
];

const selectedCount = computed(() => props.modelValue.length);

const isSelected = (status: OrderStatusEnum) => {
  return props.modelValue.includes(status);
};

const toggleDropdown = () => {
  if (!props.disabled) {
    isOpen.value = !isOpen.value;
  }
};

const closeDropdown = () => {
  isOpen.value = false;
};

const toggleStatus = (status: OrderStatusEnum) => {
  const newValue = [...props.modelValue];
  const index = newValue.indexOf(status);
  
  if (index > -1) {
    newValue.splice(index, 1);
  } else {
    newValue.push(status);
  }
  
  emit('update:modelValue', newValue);
};

const clearSelection = () => {
  emit('update:modelValue', []);
};

const selectAll = () => {
  emit('update:modelValue', availableStatuses.map(s => s.value));
};

const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (!target.closest('.status-filter-container')) {
    closeDropdown();
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped lang="scss">
.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  
  .filter-label {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--color-text-700);
    white-space: nowrap;
    text-align: right;
    margin-bottom: 0;
  }
}

.status-filter-container {
  position: relative;
  flex-grow: 1;
}

.status-filter-toggle {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 2px solid var(--color-text-300);
  border-radius: 4px;
  background: white;
  font-size: 0.8rem;
  height: 2.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
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
    cursor: not-allowed;
    opacity: 0.6;
  }
  
  .arrow {
    transition: transform 0.2s;
    font-size: 0.7em;
    
    &.open {
      transform: rotate(180deg);
    }
  }
}

.status-dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: white;
  border: 1px solid var(--color-text-300);
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 100;
  max-height: 300px;
  overflow-y: auto;
}

.status-options {
  padding: 0.5rem;
}

.status-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
  
  &:hover {
    background-color: var(--color-background-100);
  }
  
  input[type="checkbox"] {
    cursor: pointer;
  }
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
  
  &.status-new {
    background: var(--color-info-100);
    color: var(--color-info-700);
  }
  
  &.status-processing {
    background: var(--color-warning-100);
    color: var(--color-warning-700);
  }
  
  &.status-ready {
    background: var(--color-success-100);
    color: var(--color-success-700);
  }
  
  &.status-done {
    background: var(--color-primary-100);
    color: var(--color-primary-700);
  }
  
  &.status-cancelled {
    background: var(--color-error-100);
    color: var(--color-error-700);
  }
  
  &.status-error {
    background: var(--color-error-100);
    color: var(--color-error-700);
  }
  
  &.status-archived {
    background: var(--color-text-100);
    color: var(--color-text-600);
  }
}

.dropdown-footer {
  display: flex;
  gap: 0.5rem;
  padding: 0.5rem;
  border-top: 1px solid var(--color-text-200);
  background: var(--color-background-100);
}

.clear-btn,
.select-all-btn {
  flex: 1;
  padding: 0.375rem 0.5rem;
  border: 1px solid var(--color-text-300);
  border-radius: 4px;
  background: white;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    background: var(--color-background-200);
    border-color: var(--color-text-400);
  }
}

.select-all-btn {
  background: var(--color-primary-500);
  color: white;
  border-color: var(--color-primary-500);
  
  &:hover {
    background: var(--color-primary-600);
    border-color: var(--color-primary-600);
  }
}
</style>