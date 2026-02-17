<template>
  <div v-if="isOpen" class="modal-overlay" @click="close">
    <div class="modal-content large" @click.stop>
      <div class="modal-header">
        <h3>Детали заказа #{{ orderId }}</h3>
        <button class="close-btn" @click="close" aria-label="Закрыть">
          &times;
        </button>
      </div>

      <div v-if="loading" class="loading-state">
        Загрузка деталей заказа...
      </div>

      <div v-else-if="error" class="error-state">
        {{ error }}
      </div>

      <div v-else-if="order" class="order-details">
        <div class="section">
          <h4>Информация о читателе</h4>
          <div class="info-grid">
            <div class="info-item">
              <strong>ФИО:</strong> {{ order.user.fullname }}
            </div>
            <div class="info-item">
              <strong>Подразделение:</strong> {{ order.user.department }}
            </div>
            <div class="info-item">
              <strong>Читательский билет:</strong> {{ order.user.library_card || 'Не указан' }}
            </div>
            <div class="info-item">
              <strong>Campus ID:</strong> {{ order.user.campus_id || 'Не указан' }}
            </div>
            <div class="info-item">
              <strong>MIRA ID:</strong> {{ order.user.mira_id || 'Не указан' }}
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
            <div class="info-item">
              <strong>Дата создания:</strong> {{ formatDateTime(order.statuses[0]?.date) }}
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
              <div class="status-dot" :class="getStatusClass(status.status)"></div>
              <div class="status-content">
                <div class="status-header">
                  <div class="status-type">{{ getStatusText(status.status) }}</div>
                  <div class="status-date">{{ formatDateTime(status.date) }}</div>
                </div>
                <div class="status-staff">
                  Сотрудник: {{ status.staff.fullname }}
                </div>
                <div v-if="status.description" class="status-description">
                  {{ status.description }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="section">
          <h4>Книги в заказе ({{ order.books?.length || 0 }})</h4>
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
                <div class="book-meta">
                  <span class="book-id">ID: {{ bookItem.book.id }}</span>
                  <span v-if="bookItem.book.year" class="book-year">
                    • Год: {{ bookItem.book.year }}
                  </span>
                </div>
              </div>
              <div class="book-status-info">
                <span class="status-badge small" :class="getBookStatusClass(bookItem.status)">
                  {{ getBookStatusText(bookItem.status) }}
                </span>
                <div v-if="bookItem.handed_date" class="book-dates">
                  <div>Выдана: {{ formatDate(bookItem.handed_date) }}</div>
                  <div v-if="bookItem.to_return_date">
                    Вернуть до: {{ formatDate(bookItem.to_return_date) }}
                  </div>
                  <div v-if="bookItem.returned_date">
                    Возвращена: {{ formatDate(bookItem.returned_date) }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="order.books_to_return && order.books_to_return.length > 0" class="section">
          <h4>Книги к возврату ({{ order.books_to_return.length }})</h4>
          <div class="books-list">
            <div 
              v-for="bookItem in order.books_to_return" 
              :key="bookItem.id"
              class="book-item warning"
            >
              <div class="book-main-info">
                <div class="book-title">
                  {{ bookItem.book.title?.[0] || 'Без названия' }}
                </div>
                <div class="book-authors">
                  {{ bookItem.book.author?.join(', ') || 'Автор не указан' }}
                </div>
              </div>
              <div class="book-status-info">
                <span class="status-badge small status-warning">
                  Требуется возврат
                </span>
                <div class="book-dates">
                  <div>Выдана: {{ formatDate(bookItem.handed_date) }}</div>
                  <div class="overdue">
                    Вернуть до: {{ formatDate(bookItem.to_return_date) }}
                  </div>
                </div>
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
import { ref, watch, computed } from 'vue';
import type { Order } from "@api/types";
import { orderStatuses, orderBookStatuses } from "@api/types";
import { getModeratorOrderDetail } from "@api/orders";

interface Props {
  isOpen: boolean;
  orderId: number;
}

interface Emits {
  (e: 'update:isOpen', value: boolean): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const order = ref<Order | null>(null);
const loading = ref(false);
const error = ref('');

const currentStatus = computed(() => {
  if (!order.value?.statuses || order.value.statuses.length === 0) return 'unknown';
  return order.value.statuses[order.value.statuses.length - 1].status;
});

const close = () => {
  emit('update:isOpen', false);
};

const loadOrderDetails = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    order.value = await getModeratorOrderDetail(props.orderId);
  } catch (err: any) {
    console.error('Ошибка загрузки деталей заказа:', err);
    error.value = 'Не удалось загрузить детали заказа. Попробуйте позже.';
  } finally {
    loading.value = false;
  }
};

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
  if (!dateString) return '—';
  return new Date(dateString).toLocaleString('ru-RU');
};

const formatDate = (dateString: string | null) => {
  if (!dateString) return '—';
  return new Date(dateString).toLocaleDateString('ru-RU');
};

watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    loadOrderDetails();
  } else {
    order.value = null;
    error.value = '';
  }
}, { immediate: true });
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
  overflow-y: auto;
  padding: 20px;
}

.modal-content.large {
  background: white;
  border-radius: 8px;
  width: 95%;
  max-width: 900px;
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
  position: sticky;
  top: 0;
  background: white;
  z-index: 1;
  
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
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
  
  &:hover {
    color: var(--color-text-800);
    background: var(--color-background-200);
  }
}

.loading-state,
.error-state {
  padding: 3rem;
  text-align: center;
  color: var(--color-text-600);
}

.error-state {
  color: var(--color-error-600);
}

.order-details {
  padding: 1.5rem;
}

.section {
  margin-bottom: 2rem;
  
  &:last-child {
    margin-bottom: 0;
  }
  
  h4 {
    margin: 0 0 1rem 0;
    color: var(--color-text-800);
    border-bottom: 2px solid var(--color-text-200);
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
  position: relative;
  padding-left: 2rem;
  
  &::before {
    content: '';
    position: absolute;
    left: 6px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--color-text-200);
  }
  
  .status-item {
    position: relative;
    margin-bottom: 1.5rem;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  .status-dot {
    position: absolute;
    left: -2rem;
    top: 0.25rem;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: var(--color-text-400);
    border: 2px solid white;
    z-index: 1;
    
    &.status-new {
      background: var(--color-info-500);
    }
    
    &.status-processing {
      background: var(--color-warning-500);
    }
    
    &.status-ready {
      background: var(--color-success-500);
    }
    
    &.status-done {
      background: var(--color-primary-500);
    }
    
    &.status-cancelled,
    &.status-error {
      background: var(--color-error-500);
    }
  }
  
  .status-content {
    background: var(--color-background-100);
    padding: 1rem;
    border-radius: 4px;
    border-left: 3px solid var(--color-text-300);
  }
  
  .status-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.5rem;
    gap: 1rem;
  }
  
  .status-type {
    font-weight: 600;
    color: var(--color-text-800);
  }
  
  .status-date {
    font-size: 0.875rem;
    color: var(--color-text-600);
    white-space: nowrap;
  }
  
  .status-staff {
    font-size: 0.875rem;
    color: var(--color-text-700);
    margin-bottom: 0.25rem;
  }
  
  .status-description {
    font-size: 0.875rem;
    color: var(--color-text-600);
    font-style: italic;
  }
}

.books-list {
  .book-item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
    border: 1px solid var(--color-text-200);
    border-radius: 4px;
    margin-bottom: 0.5rem;
    background: white;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    &.warning {
      border-color: var(--color-warning-400);
      background: var(--color-warning-50);
    }
  }
  
  .book-main-info {
    flex: 1;
  }
  
  .book-title {
    font-weight: 600;
    color: var(--color-text-800);
    margin-bottom: 0.25rem;
    line-height: 1.4;
  }
  
  .book-authors {
    font-size: 0.875rem;
    color: var(--color-text-600);
    margin-bottom: 0.25rem;
  }
  
  .book-meta {
    font-size: 0.75rem;
    color: var(--color-text-500);
    
    .book-id,
    .book-year {
      display: inline;
    }
  }
  
  .book-status-info {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
  }
  
  .book-dates {
    font-size: 0.75rem;
    color: var(--color-text-600);
    text-align: right;
    
    div {
      margin-bottom: 0.25rem;
      
      &:last-child {
        margin-bottom: 0;
      }
    }
    
    .overdue {
      color: var(--color-error-600);
      font-weight: 500;
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
  
  &.status-cancelled,
  &.status-error {
    background: var(--color-error-100);
    color: var(--color-error-700);
  }
  
  &.status-archived {
    background: var(--color-text-100);
    color: var(--color-text-600);
  }
  
  &.status-ordered {
    background: var(--color-info-100);
    color: var(--color-info-700);
  }
  
  &.status-handed {
    background: var(--color-success-100);
    color: var(--color-success-700);
  }
  
  &.status-returned {
    background: var(--color-primary-100);
    color: var(--color-primary-700);
  }
  
  &.status-warning {
    background: var(--color-warning-100);
    color: var(--color-warning-700);
  }
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--color-text-200);
  display: flex;
  justify-content: flex-end;
  position: sticky;
  bottom: 0;
  background: white;
}

.close-modal-btn {
  background: var(--color-primary-500);
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.2s;
  
  &:hover {
    background: var(--color-primary-600);
  }
}
</style>