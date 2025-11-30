<template>
  <div class="filter-group">
    <label class="filter-label">{{ label }}</label>
    <div class="dropdown-container" ref="dropdownContainer">
      <div 
        class="dropdown-trigger"
        :class="{ 'dropdown-open': isOpen, 'dropdown-disabled': disabled }"
        @click="toggleDropdown"
      >
        <span class="dropdown-selected">
          {{ selectedText }}
        </span>
        <span class="dropdown-arrow">▼</span>
      </div>
      
      <div v-if="isOpen" class="dropdown-menu">
        <div 
          v-for="status in statusOptions" 
          :key="status.value"
          class="dropdown-item"
          :class="{ 'dropdown-item-selected': isSelected(status.value) }"
          @click="toggleStatus(status.value)"
        >
          <span class="checkbox-indicator">
            {{ isSelected(status.value) ? '✓' : '' }}
          </span>
          <span class="dropdown-item-label">{{ status.label }}</span>
        </div>
        
        <div class="dropdown-actions" v-if="localValue.length > 0">
          <button 
            @click.stop="clearAll"
            class="clear-all-btn"
            type="button"
          >
            Сбросить все
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { orderStatuses, type OrderStatusEnum } from '@api/types';

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
const dropdownContainer = ref<HTMLElement>();

const localValue = computed({
  get: () => props.modelValue || [],
  set: (value) => emit('update:modelValue', value)
});

const statusOptions = computed(() => {
  return Object.entries(orderStatuses).map(([value, label]) => ({
    value: value as OrderStatusEnum,
    label
  }));
});

const selectedText = computed(() => {
  const selected = localValue.value || [];
  if (selected.length === 0) {
    return 'Выберите статусы...';
  }
  if (selected.length === statusOptions.value.length) {
    return 'Все статусы';
  }
  if (selected.length <= 2) {
    return selected.map(statusValue => {
      const status = statusOptions.value.find(s => s.value === statusValue);
      return status ? status.label : statusValue;
    }).join(', ');
  }
  return `Выбрано: ${selected.length}`;
});

const isSelected = (statusValue: OrderStatusEnum) => {
  return localValue.value.includes(statusValue);
};

const toggleStatus = (statusValue: OrderStatusEnum) => {
  const currentValue = [...localValue.value];
  const index = currentValue.indexOf(statusValue);
  
  if (index > -1) {
    currentValue.splice(index, 1);
  } else {
    currentValue.push(statusValue);
  }
  
  localValue.value = currentValue;
};

const toggleDropdown = () => {
  if (!props.disabled) {
    isOpen.value = !isOpen.value;
  }
};

const clearAll = () => {
  localValue.value = [];
};

const handleClickOutside = (event: MouseEvent) => {
  if (dropdownContainer.value && !dropdownContainer.value.contains(event.target as Node)) {
    isOpen.value = false;
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
  flex-direction: column;
  gap: 0.25rem;
  position: relative;
  
  .filter-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--color-text-700);
    margin-bottom: 0.25rem;
  }
}

.dropdown-container {
  position: relative;
  width: 100%;
}

.dropdown-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-text-300);
  border-radius: 4px;
  background: white;
  font-size: 0.875rem;
  height: 2.25rem;
  cursor: pointer;
  transition: border-color 0.2s ease;
  
  &:hover:not(.dropdown-disabled) {
    border-color: var(--color-primary-500);
  }
  
  &.dropdown-open {
    border-color: var(--color-primary-500);
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
  
  &.dropdown-disabled {
    background: var(--color-background-300);
    cursor: not-allowed;
    opacity: 0.6;
  }
}

.dropdown-selected {
  color: var(--color-text-800);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.dropdown-arrow {
  color: var(--color-text-500);
  font-size: 0.75rem;
  margin-left: 0.5rem;
  transition: transform 0.2s ease;
  
  .dropdown-open & {
    transform: rotate(180deg);
  }
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid var(--color-text-300);
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  margin-top: 2px;
  max-height: 200px;
  overflow-y: auto;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid var(--color-text-100);
  
  &:last-child {
    border-bottom: none;
  }
  
  &:hover {
    background: var(--color-primary-50);
  }
  
  &.dropdown-item-selected {
    background: var(--color-primary-50);
    color: var(--color-primary-700);
  }
}

.checkbox-indicator {
  width: 1rem;
  height: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
  color: var(--color-primary-600);
  flex-shrink: 0;
}

.dropdown-item-label {
  font-size: 0.875rem;
  color: inherit;
}

.dropdown-actions {
  padding: 0.5rem 0.75rem;
  border-top: 1px solid var(--color-text-200);
  background: var(--color-background-100);
}

.clear-all-btn {
  background: none;
  border: none;
  color: var(--color-error-500);
  font-size: 0.75rem;
  cursor: pointer;
  padding: 0.25rem 0;
  
  &:hover {
    color: var(--color-error-600);
    text-decoration: underline;
  }
}
</style>