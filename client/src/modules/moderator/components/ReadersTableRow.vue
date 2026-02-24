<template>
  <tr class="reader-row" @click="handleRowClick">
    <td 
      :class="{ expanded: isExpanded }" 
      @contextmenu="showContextMenu"
    >
      {{ reader.library_card }}
      
      <div 
        v-if="showMenu" 
        class="context-menu" 
        :style="menuStyle"
        @click.stop
      >
        <div class="menu-item" @click="toggleExpand">
          {{ isExpanded ? 'Свернуть' : 'Раскрыть' }}
        </div>
        <div class="menu-item" @click="copyToClipboard">
          Копировать
        </div>
      </div>
    </td>
    <td>{{ reader.fullname }}</td>
    <td>{{ reader.department }}</td>
    <td>{{ reader.total_books_ordered }}</td>
    <td>{{ reader.total_orders }}</td>
    <td>{{ reader.cancelled_orders }}</td>
  </tr>
</template>

<script setup lang="ts">
import type { ReaderStats } from "@api/types";
import { ref } from 'vue';

interface Props {
  reader: ReaderStats;
}

interface Emits {
  (e: 'row-click', reader: ReaderStats): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const isExpanded = ref(false);
const showMenu = ref(false);
const menuStyle = ref({ top: '0', left: '0' });

const handleRowClick = () => {
  emit('row-click', props.reader);
  hideContextMenu();
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
    await navigator.clipboard.writeText(props.reader.library_card || '');
    console.log('Читательский билет скопирован в буфер обмена');
    hideContextMenu();
  } catch (err) {
    console.error('Ошибка при копировании в буфер обмена:', err);
    fallbackCopyToClipboard(props.reader.library_card || '');
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

document.addEventListener('click', hideContextMenu);
document.addEventListener('contextmenu', hideContextMenu);
</script>

<style scoped lang="scss">
.reader-row {
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
    
    &:first-child {
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