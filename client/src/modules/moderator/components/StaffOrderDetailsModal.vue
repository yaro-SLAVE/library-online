<template>
  <div v-if="order" class="modal-overlay" @click="close">
    <div class="modal-content large" @click.stop>
      <div class="modal-header">
        <h3>Детали заказа #{{ order.id }}</h3>
        <button class="close-btn" @click="close" aria-label="Закрыть">
          &times;
        </button>
      </div>

      <div class="order-details">
        <div class="section">
          <h4>Информация о сотруднике</h4>
          <div class="info-grid">
            <div class="info-item">
              <strong>ФИО:</strong> {{ staff.fullname }}
            </div>
            <div class="info-item">
              <strong>Подразделение:</strong> {{ staff.department }}
            </div>
            <div class="info-item">
              <strong>Всего заказов:</strong> {{ staff.total_orders }}
            </div>
            <div class="info-item">
              <strong>Отмененные заказы:</strong> {{ staff.cancelled_orders }}
            </div>
          </div>
        </div>

        <div class="section">
          <h4>Информация о заказе</h4>
          <div class="info-grid">
            <div class="info-item">
              <strong>Библиотека:</strong> {{ order.library.description }}
            </div>
            <div class="info-item">
              <strong>Адрес:</strong> {{ order.library.address }}
            </div>
            <div class="info-item">
              <strong>Текущий статус:</strong>
              <span class="status-badge" :class="getStatusClass(currentStatus)">
                {{ getStatusText(currentStatus) }}
              </span>
            </div>
          </div>
        </div>

        <div class="section">
          <h4>История статусов</h4>
          <div class="status-timeline">
            <div 
              v-for="(status, index) in order.statuses" 
              :key="index"
              class="status-item"
            >
              <div class="status-dot"></div>
              <div class="status-content">
                <div class="status-type">{{ getStatusText(status.status) }}</div>
                <div class="status-date">{{ formatDateTime(status.date) }}</div>
                <div v-if="status.description" class="status-description">
                  {{ status.description }}
                </div>
                <div v-if="status.staff" class="status-staff">
                  Сотрудник: {{ status.staff.fullname }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="section" v-if="order.books && order.books.length > 0">
          <h4>Книги в заказе ({{ order.books.length }})</h4>
          <div class="books-list">
            <div 
              v-for="bookItem in order.books" 
              :key="bookItem.id"
              class="book-item"
            >
              <div class="book-main-info">
                <div class="book-title">
                  {{ bookItem.book.title?.[0] || 'Без названия' }}
                </div>
                <div class="book-authors">
                  {{ bookItem.book.author?.join(', ') || 'Автор не указан' }}
                </div>
                <div class="book-id">
                  ID: {{ bookItem.book.id }}
                </div>
              </div>
              <div class="book-status">
                <span class="status-badge small" :class="getBookStatusClass(bookItem.status)">
                  {{ getBookStatusText(bookItem.status) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="close-modal-btn" @click="close">
          Закрыть
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { StaffStats, Order, OrderBookStatus } from "@api/types";
import { orderStatuses, orderBookStatuses } from "@api/types";

interface Props {
  order: Order;
  staff: StaffStats;
}

interface Emits {
  (e: 'close'): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const close = () => {
  emit('close');
};

const currentStatus = computed(() => {
  if (!props.order.statuses || props.order.statuses.length === 0) return 'unknown';
  return props.order.statuses[props.order.statuses.length - 1].status;
});

const getStatusClass = (status: string) => {
  return `status-${status}`;
};

const getStatusText = (status: string) => {
  return orderStatuses[status as keyof typeof orderStatuses] || status;
};

const getBookStatusClass = (status: string) => {
  return `status-${status}`;
};

const getBookStatusText = (status: string) => {
  return orderBookStatuses[status as keyof typeof orderBookStatuses] || status;
};

const formatDateTime = (dateString: string) => {
  return new Date(dateString).toLocaleString('ru-RU');
};
</script>

<style scoped lang="scss">
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.modal-content.large {
  background: white;
  border-radius: 8px;
  width: 95%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--color-text-200);
  
  h3 {
    margin: 0;
    color: var(--color-text-800);
  }
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text-600);
  
  &:hover {
    color: var(--color-text-800);
  }
}

.order-details {
  padding: 1.5rem;
}

.section {
  margin-bottom: 2rem;
  
  h4 {
    margin: 0 0 1rem 0;
    color: var(--color-text-800);
    border-bottom: 1px solid var(--color-text-200);
    padding-bottom: 0.5rem;
  }
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.info-item {
  strong {
    color: var(--color-text-700);
    display: block;
    margin-bottom: 0.25rem;
    font-size: 0.875rem;
  }
}

.status-timeline {
  .status-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1rem;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  .status-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--color-primary-500);
    margin-right: 1rem;
    margin-top: 0.25rem;
    flex-shrink: 0;
  }
  
  .status-content {
    flex: 1;
  }
  
  .status-type {
    font-weight: 600;
    color: var(--color-text-800);
    margin-bottom: 0.25rem;
  }
  
  .status-date {
    font-size: 0.875rem;
    color: var(--color-text-600);
    margin-bottom: 0.25rem;
  }
  
  .status-description {
    font-size: 0.875rem;
    color: var(--color-text-700);
    font-style: italic;
  }
}

.books-list {
  .book-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border: 1px solid var(--color-text-200);
    border-radius: 4px;
    margin-bottom: 0.5rem;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  .book-main-info {
    flex: 1;
  }
  
  .book-title {
    font-weight: 600;
    color: var(--color-text-800);
    margin-bottom: 0.25rem;
  }
  
  .book-authors {
    font-size: 0.875rem;
    color: var(--color-text-600);
    margin-bottom: 0.25rem;
  }
  
  .book-id {
    font-size: 0.75rem;
    color: var(--color-text-500);
  }
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
  
  &.small {
    padding: 0.125rem 0.375rem;
    font-size: 0.7rem;
  }
  
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
  
  &.status-unknown {
    background: var(--color-text-100);
    color: var(--color-text-600);
  }
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--color-text-200);
  display: flex;
  justify-content: flex-end;
}

.close-modal-btn {
  background: var(--color-primary-500);
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  
  &:hover {
    background: var(--color-primary-600);
  }
}
</style>