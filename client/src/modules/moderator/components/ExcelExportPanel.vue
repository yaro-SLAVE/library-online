<script setup lang="ts">
import { ref, computed } from 'vue';
import { 
  DocumentArrowDownIcon,
  CheckCircleIcon,
  XCircleIcon 
} from '@heroicons/vue/24/outline';

interface ColumnGroup {
  name: string;
  items: ColumnItem[];
}

interface ColumnItem {
  label: string;
  value: string;
  children?: ColumnItem[];
}

const emit = defineEmits(['export']);

const columnGroups = ref<ColumnGroup[]>([
  {
    name: 'Заказы',
    items: [
      { label: 'Заказчик', value: 'customer' },
      { 
        label: 'Даты', 
        value: 'dates',
        children: [
          { label: 'Создания', value: 'creation_date' },
          { label: 'Взятия на исполнение', value: 'acceptance_date' },
          { label: 'Готовности', value: 'ready_date' },
          { label: 'Завершения', value: 'completion_date' }
        ]
      },
      { label: 'Итоговый статус', value: 'final_status' },
      { label: 'Кто собрал', value: 'assembler' },
      { label: 'Кто выдал', value: 'issuer' }
    ]
  },
  {
    name: 'Читатели',
    items: [
      { label: 'ФИО', value: 'reader_name' },
      { label: 'Подразделение', value: 'department' },
      { label: 'Блокировки', value: 'blocks' }
    ]
  },
  {
    name: 'Книги заказов',
    items: [
      { label: 'Инвентарный номер', value: 'inventory_number' },
      { label: 'Номер карты комплектования', value: 'kit_card_number' },
      { label: 'Коротко о книге', value: 'book_summary' }
    ]
  },
  {
    name: 'Сотрудники',
    items: [
      { label: 'ФИО', value: 'employee_name' },
      { label: 'Филиал', value: 'branch' }
    ]
  }
]);

const selectedColumns = ref<Set<string>>(new Set());
const isExporting = ref(false);
const exportStatus = ref<'idle' | 'success' | 'error'>('idle');

const selectionStats = computed(() => {
  const total = columnGroups.value.reduce((acc, group) => {
    let count = 0;
    const countItems = (items: ColumnItem[]) => {
      items.forEach(item => {
        count++;
        if (item.children) countItems(item.children);
      });
    };
    countItems(group.items);
    return acc + count;
  }, 0);

  return {
    selected: selectedColumns.value.size,
    total
  };
});

const toggleColumn = (value: string) => {
  if (selectedColumns.value.has(value)) {
    selectedColumns.value.delete(value);
  } else {
    selectedColumns.value.add(value);
  }
};

const toggleAllInGroup = (group: ColumnGroup, select: boolean) => {
  const toggleItems = (items: ColumnItem[]) => {
    items.forEach(item => {
      if (select) {
        selectedColumns.value.add(item.value);
      } else {
        selectedColumns.value.delete(item.value);
      }
      if (item.children) {
        toggleItems(item.children);
      }
    });
  };
  
  toggleItems(group.items);
};

const selectAll = () => {
  columnGroups.value.forEach(group => toggleAllInGroup(group, true));
};

const clearAll = () => {
  selectedColumns.value.clear();
};

const handleExport = async () => {
  if (selectedColumns.value.size === 0) return;

  isExporting.value = true;
  exportStatus.value = 'idle';

  try {
    await emit('export', Array.from(selectedColumns.value));
    exportStatus.value = 'success';
    
    setTimeout(() => {
      exportStatus.value = 'idle';
    }, 3000);
  } catch (error) {
    console.error('Export failed:', error);
    exportStatus.value = 'error';
    
    setTimeout(() => {
      exportStatus.value = 'idle';
    }, 3000);
  } finally {
    isExporting.value = false;
  }
};
</script>

<template>
  <div class="excel-export-panel">
    <!-- Заголовок панели -->
    <div class="panel-header">
      <div class="header-main">
        <DocumentArrowDownIcon class="header-icon" />
        <div class="header-text">
          <h3>Экспорт в Excel</h3>
          <p>Выберите данные для включения в отчет</p>
        </div>
      </div>
      <div class="selection-stats">
        <span class="stats-text">
          Выбрано: {{ selectionStats.selected }} из {{ selectionStats.total }}
        </span>
      </div>
    </div>

    <!-- Глобальные действия -->
    <div class="global-actions">
      <button @click="selectAll" class="action-btn select-all-btn">
        Выбрать все
      </button>
      <button @click="clearAll" class="action-btn clear-all-btn">
        Очистить все
      </button>
    </div>

    <div class="columns-selection">
      <div 
        v-for="group in columnGroups" 
        :key="group.name"
        class="column-group"
      >
        <div class="group-header">
          <h4 class="group-title">{{ group.name }}</h4>
          <div class="group-actions">
            <button 
              @click="toggleAllInGroup(group, true)"
              class="group-action-btn"
            >
              Выбрать все
            </button>
            <button 
              @click="toggleAllInGroup(group, false)"
              class="group-action-btn"
            >
              Очистить
            </button>
          </div>
        </div>
        
        <div class="column-items">
          <div 
            v-for="item in group.items" 
            :key="item.value"
            class="column-item"
          >
            <label class="checkbox-label main-checkbox">
              <input
                type="checkbox"
                :checked="selectedColumns.has(item.value)"
                @change="toggleColumn(item.value)"
              />
              <span class="custom-checkbox"></span>
              <span class="checkbox-text">{{ item.label }}</span>
            </label>
            
            <div v-if="item.children" class="nested-items">
              <label
                v-for="child in item.children"
                :key="child.value"
                class="checkbox-label nested-checkbox"
              >
                <input
                  type="checkbox"
                  :checked="selectedColumns.has(child.value)"
                  @change="toggleColumn(child.value)"
                />
                <span class="custom-checkbox"></span>
                <span class="checkbox-text">{{ child.label }}</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="export-actions">
      <div class="export-status" v-if="exportStatus !== 'idle'">
        <CheckCircleIcon 
          v-if="exportStatus === 'success'" 
          class="status-icon success" 
        />
        <XCircleIcon 
          v-if="exportStatus === 'error'" 
          class="status-icon error" 
        />
        <span class="status-text">
          {{
            exportStatus === 'success' 
              ? 'Файл успешно сформирован!' 
              : 'Ошибка при формировании файла'
          }}
        </span>
      </div>

      <button 
        @click="handleExport"
        :disabled="selectedColumns.size === 0 || isExporting"
        class="export-button"
        :class="{
          'disabled': selectedColumns.size === 0,
          'exporting': isExporting,
          'success': exportStatus === 'success',
          'error': exportStatus === 'error'
        }"
      >
        <DocumentArrowDownIcon class="button-icon" />
        <span v-if="!isExporting">
          Скачать Excel ({{ selectedColumns.size }})
        </span>
        <span v-else class="exporting-text">
          Формируем отчет...
        </span>
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.excel-export-panel {
  background: var(--color-background-100);
  border-radius: 16px;
  border: 1px solid var(--color-background-200);
  overflow: hidden;
}

.panel-header {
  padding: 2rem;
  background: linear-gradient(
    135deg,
    var(--color-primary-50) 0%,
    var(--color-background-100) 100%
  );
  border-bottom: 1px solid var(--color-background-200);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;

  .header-main {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .header-icon {
    width: 2.5rem;
    height: 2.5rem;
    color: var(--color-primary-500);
  }

  .header-text {
    h3 {
      margin: 0 0 0.25rem 0;
      color: var(--color-primary-700);
      font-size: 1.5rem;
      font-weight: 600;
    }

    p {
      margin: 0;
      color: var(--color-text-600);
      font-size: 1rem;
    }
  }

  .selection-stats {
    .stats-text {
      color: var(--color-primary-600);
      font-weight: 500;
      font-size: 0.95rem;
      padding: 0.5rem 1rem;
      background: var(--color-primary-100);
      border-radius: 8px;
      border: 1px solid var(--color-primary-200);
    }
  }
}

.global-actions {
  padding: 1.5rem 2rem;
  background: var(--color-background-50);
  border-bottom: 1px solid var(--color-background-200);
  display: flex;
  gap: 1rem;

  .action-btn {
    padding: 0.75rem 1.5rem;
    border: 1px solid;
    border-radius: 10px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.95rem;

    &.select-all-btn {
      background: var(--color-primary-500);
      color: var(--color-text-50);
      border-color: var(--color-primary-500);

      &:hover {
        background: var(--color-primary-600);
        border-color: var(--color-primary-600);
        transform: translateY(-1px);
      }
    }

    &.clear-all-btn {
      background: transparent;
      color: var(--color-text-600);
      border-color: var(--color-background-300);

      &:hover {
        background: var(--color-background-200);
        border-color: var(--color-background-400);
      }
    }
  }
}

.columns-selection {
  padding: 2rem;
  max-height: 600px;
  overflow-y: auto;
}

.column-group {
  margin-bottom: 2.5rem;

  &:last-child {
    margin-bottom: 0;
  }
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--color-primary-200);

  .group-title {
    margin: 0;
    color: var(--color-primary-700);
    font-size: 1.2rem;
    font-weight: 600;
  }

  .group-actions {
    display: flex;
    gap: 0.75rem;
  }

  .group-action-btn {
    background: transparent;
    border: 1px solid var(--color-primary-300);
    color: var(--color-primary-600);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      background: var(--color-primary-50);
      border-color: var(--color-primary-400);
    }
  }
}

.column-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.column-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.875rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;

  &:hover {
    background: var(--color-background-50);
    border-color: var(--color-background-300);
  }

  &.main-checkbox {
    background: var(--color-background-50);
    border: 1px solid var(--color-background-200);
    font-weight: 500;
    color: var(--color-text-800);
  }

  &.nested-checkbox {
    margin-left: 2rem;
    font-size: 0.95rem;
    color: var(--color-text-700);

    &:hover {
      background: var(--color-primary-50);
      border-color: var(--color-primary-100);
    }
  }
}

.custom-checkbox {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-primary-300);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  background: white;
  flex-shrink: 0;
}

input[type="checkbox"] {
  display: none;

  &:checked + .custom-checkbox {
    background: var(--color-primary-500);
    border-color: var(--color-primary-500);

    &::after {
      content: '✓';
      color: white;
      font-size: 12px;
      font-weight: bold;
    }
  }
}

.checkbox-text {
  flex: 1;
}

.nested-items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-left: 1rem;
}

.export-actions {
  padding: 2rem;
  border-top: 1px solid var(--color-background-200);
  background: var(--color-background-50);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.export-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;

  .status-icon {
    width: 1.25rem;
    height: 1.25rem;

    &.success {
      color: var(--color-primary-500);
    }

    &.error {
      color: var(--color-accent-500);
    }
  }

  .status-text {
    font-size: 0.95rem;
  }
}

.export-button {
  background: linear-gradient(
    135deg,
    var(--color-primary-500) 0%,
    var(--color-primary-600) 100%
  );
  color: var(--color-text-50);
  border: none;
  padding: 1rem 2.5rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  box-shadow: 0 4px 12px rgba(102, 69, 186, 0.3);

  &:hover:not(.disabled):not(.exporting) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 69, 186, 0.4);
    background: linear-gradient(
      135deg,
      var(--color-primary-600) 0%,
      var(--color-primary-700) 100%
    );
  }

  &.disabled {
    background: var(--color-background-300);
    color: var(--color-text-400);
    cursor: not-allowed;
    box-shadow: none;
  }

  &.exporting {
    background: var(--color-primary-400);
    cursor: wait;
  }

  &.success {
    background: var(--color-primary-500);
  }

  &.error {
    background: var(--color-accent-500);
  }

  .button-icon {
    width: 1.25rem;
    height: 1.25rem;
  }

  .exporting-text {
    display: flex;
    align-items: center;
    gap: 0.5rem;

    &::after {
      content: '';
      width: 1rem;
      height: 1rem;
      border: 2px solid transparent;
      border-top: 2px solid currentColor;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.columns-selection::-webkit-scrollbar {
  width: 8px;
}

.columns-selection::-webkit-scrollbar-track {
  background: var(--color-background-50);
  border-radius: 4px;
}

.columns-selection::-webkit-scrollbar-thumb {
  background: var(--color-primary-300);
  border-radius: 4px;
}

.columns-selection::-webkit-scrollbar-thumb:hover {
  background: var(--color-primary-400);
}

/* Адаптивность */
@media (max-width: 768px) {
  .panel-header {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
    gap: 1.5rem;
  }

  .global-actions {
    justify-content: center;
    flex-wrap: wrap;
  }

  .group-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .group-actions {
    justify-content: center;
  }

  .nested-items {
    margin-left: 0.5rem;
  }

  .checkbox-label.nested-checkbox {
    margin-left: 1.5rem;
  }

  .export-button {
    min-width: auto;
    width: 100%;
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .panel-header,
  .columns-selection,
  .export-actions {
    padding: 1.5rem;
  }

  .global-actions {
    padding: 1rem 1.5rem;
  }
}
</style>