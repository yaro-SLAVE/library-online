<template>
  <tr class="order-row" @click="handleRowClick">
    <td>{{ order.id }}</td>
    <td>{{ order.fullname }}</td>
    <td 
      :class="{ expanded: isExpanded }" 
      @contextmenu="showContextMenu"
    >
      {{ order.library_card || '—' }}
      
      <div 
        v-if="showMenu" 
        class="context-menu" 
        :style="menuStyle"
        @click.stop
      >
        <div class="menu-item" @click="toggleExpand">
          {{ isExpanded ? 'Свернуть' : 'Раскрыть' }}
        </div>
        <div class="menu-item" @click="copyToClipboard" v-if="order.library_card">
          Копировать
        </div>
      </div>
    </td>
    <td>{{ order.library_name }}</td>
    <td>
      <span class="status-badge" :class="getStatusClass(order.current_status)">
        {{ getStatusText(order.current_status) }}
      </span>
    </td>
    <td class="center">{{ order.books_count }}</td>
    <td>{{ order.employee_collect }}</td>
    <td>{{ order.employee_issue }}</td>
    <td>{{ formatDate(order.created_date) }}</td>
  </tr>
</template>

<script setup lang="ts">
import type { ModeratorOrderStats } from "@api/types";
import { orderStatuses } from "@api/types";
import { ref, onMounted, onUnmounted } from 'vue';

interface Props {
  order: ModeratorOrderStats;
}

interface Emits {
  (e: 'row-click', order: ModeratorOrderStats): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const isExpanded = ref(false);
const showMenu = ref(false);
const menuStyle = ref({ top: '0', left: '0' });

const handleRowClick = () => {
  emit('row-click', props.order);
  hideContextMenu();
};

const getStatusClass = (status: string) => {
  return `status-${status}`;
};

const getStatusText = (status: string) => {
  return orderStatuses[status as keyof typeof orderStatuses] || status;
};

const formatDate = (dateString: string) => {
  if (!dateString) return '—';
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const showContextMenu = (event: MouseEvent) => {
  event.preventDefault();
  event.stopPropagation();
  
  menuStyle.value = {
    top: `${event.clientY}px`,
    left: `${event.clientX}px`
  };
  showMenu.value = true;
};

const hideContextMenu = () => {
  showMenu.value = false;
};

const toggleExpand = () => {
  isExpanded.value = !isExpanded.value;
  hideContextMenu();
};

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(props.order.library_card || '');
    console.log('Читательский билет скопирован в буфер обмена');
    hideContextMenu();
  } catch (err) {
    console.error('Ошибка при копировании в буфер обмена:', err);
    fallbackCopyToClipboard(props.order.library_card || '');
    hideContextMenu();
  }
};

const fallbackCopyToClipboard = (text: string) => {
  const textArea = document.createElement('textarea');
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.select();
  try {
    document.execCommand('copy');
    console.log('Читательский билет скопирован (fallback)');
  } catch (err) {
    console.error('Fallback copying failed:', err);
  }
  document.body.removeChild(textArea);
};

onMounted(() => {
  document.addEventListener('click', hideContextMenu);
  document.addEventListener('contextmenu', hideContextMenu);
});
onUnmounted(() => {
  document.removeEventListener('click', hideContextMenu);
  document.removeEventListener('contextmenu', hideContextMenu);
});
</script>

<style scoped lang="scss">
.order-row {
  cursor: pointer;
  transition: background-color 0.2s;
  background-color: var(--color-background-100);
  position: relative;
  
  &:hover {
    background-color: var(--color-background-200);
  }
  
  td {
    padding: 12px;
    text-align: left;
    color: var(--color-text-800);
    border-bottom: 1px solid var(--color-text-200);
    background-color: transparent;
    vertical-align: middle;
    position: relative;
    
    &.center {
      text-align: center;
    }
    
    &:nth-child(3) {
      width: 120px;
      min-width: 120px;
      max-width: 120px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      cursor: context-menu;
      transition: all 0.3s ease;
      
      &.expanded {
        width: auto;
        min-width: auto;
        max-width: none;
        white-space: normal;
        overflow: visible;
      }
    }
  }
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
  display: inline-block;
  
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

.context-menu {
  position: fixed;
  background: white;
  border: 1px solid var(--color-text-200);
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  min-width: 150px;
}

.menu-item {
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
  
  &:hover {
    background-color: var(--color-background-100);
  }
  
  &:not(:last-child) {
    border-bottom: 1px solid var(--color-text-100);
  }
}
</style>