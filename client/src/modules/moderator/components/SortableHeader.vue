<template>
  <th
    @click="handleClick"
    class="sortable-th"
    :class="headerClasses"
    :aria-sort="ariaSort"
    role="columnheader"
    tabindex="0"
    @keydown.enter="handleClick"
    @keydown.space.prevent="handleClick"
  >
    <span class="th-content">
      <slot />
      <span class="th-icon">
        <span v-if="isActive" class="direction-icon">
          {{ direction === 'asc' ? "↓" : "↑" }}
        </span>
        <span v-else>⇅</span>
      </span>
    </span>
  </th>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  field: string;
  currentField: string;
  direction: 'asc' | 'desc';
  loading: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  sort: [field: string, direction: 'asc' | 'desc']
}>();

const isActive = computed(() => props.currentField === props.field);

const headerClasses = computed(() => ({
  'active-sort': isActive.value,
  'sort-loading': props.loading,
  'sort-asc': isActive.value && props.direction === 'asc',
  'sort-desc': isActive.value && props.direction === 'desc'
}));

const ariaSort = computed(() => {
  if (!isActive.value) return 'none';
  return props.direction === 'asc' ? 'ascending' : 'descending';
});

const handleClick = () => {
  if (props.loading) return;
  
  if (isActive.value) {
    const newDirection = props.direction === 'asc' ? 'desc' : 'asc';
    emit('sort', props.field, newDirection);
  } else {
    emit('sort', props.field, 'asc');
  }
};
</script>

<style scoped lang="scss">
.sortable-th {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
  position: relative;

  &:hover:not(.sort-loading) {
    background-color: var(--color-background-200);
  }

  &:focus {
    outline: 2px solid var(--color-primary-500);
    outline-offset: -2px;
  }

  &.active-sort {
    background-color: var(--color-background-300);
    
    .th-icon {
      opacity: 1;
      font-weight: bold;
    }
  }

  &.sort-loading {
    cursor: wait;
    opacity: 0.7;
  }

  &.sort-asc .direction-icon {
    color: var(--color-success-500);
  }

  &.sort-desc .direction-icon {
    color: var(--color-success-500);
  }
}

.th-content {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.th-icon {
  font-size: 0.9em;
  opacity: 0.7;
  transition: opacity 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1em;
  height: 1em;
}

.direction-icon {
  font-weight: bold;
}
</style>