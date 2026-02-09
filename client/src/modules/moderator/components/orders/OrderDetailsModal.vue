<!-- OrderDetailsModal.vue -->
<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content large" @click.stop>
      <div class="modal-header">
        <h3>Детали заказа #{{ order?.id ?? orderId }}</h3>
        <button class="close-btn" @click="closeModal" aria-label="Закрыть">
          &times;
        </button>
      </div>

      <div class="order-details">
        <div v-if="error" class="section">
          <h4>Ошибка</h4>
          <p>{{ error }}</p>
        </div>

        <div v-else-if="!order" class="section">
          <p>Загрузка...</p>
        </div>

        <div v-else>
          <div class="section">
            <h4>Информация о читателе</h4>
            <div class="info-grid">
              <div class="info-item">
                <strong>ФИО:</strong>
                {{ order.user?.fullname || `${order.user?.first_name || ''} ${order.user?.last_name || ''}`.trim() || 'Не указано' }}
              </div>
              <div class="info-item">
                <strong>Подразделение:</strong>
                {{ order.user?.department ?? 'Не указано' }}
              </div>
              <div class="info-item">
                <strong>Читательский билет:</strong>
                {{ order.user?.library_card ?? 'Не указан' }}
              </div>
            </div>
          </div>

          <div class="section">
            <h4>Информация о заказе</h4>
            <div class="info-grid">
              <div class="info-item">
                <strong>Библиотека:</strong> {{ order.library?.description ?? '-' }}
              </div>
              <div class="info-item">
                <strong>Адрес:</strong> {{ order.library?.address ?? '-' }}
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
            <div v-if="Array.isArray(order.statuses) && order.statuses.length > 0" class="status-timeline">
              <div
                v-for="(st, idx) in order.statuses"
                :key="st.date ?? idx"
                class="status-item"
              >
                <div class="status-dot"></div>
                <div class="status-content">
                  <div class="status-type">{{ getStatusText(st.status) }}</div>
                  <div class="status-date">{{ formatDateTime(st.date) }}</div>
                  <div v-if="st.description" class="status-description">
                    {{ st.description }}
                  </div>
                  <div v-else-if="st.staff?.fullname" class="status-description">
                    {{ st.staff.fullname }}
                  </div>
                </div>
              </div>
            </div>
            <div v-else>
              <p>История статусов отсутствует.</p>
            </div>
          </div>

          <div class="section">
            <h4>Книги в заказе ({{ order.books?.length ?? 0 }})</h4>
            <div v-if="Array.isArray(order.books) && order.books.length > 0" class="books-list">
              <div
                v-for="bookItem in order.books"
                :key="bookItem.id"
                class="book-item"
              >
                <div class="book-main-info">
                  <div class="book-title">
                    {{ bookItem.book?.title ?? 'Без названия' }}
                  </div>
                  <div class="book-authors">
                    {{ (bookItem.book?.author && bookItem.book.author.length) ? bookItem.book.author.join(', ') : 'Автор не указан' }}
                  </div>
                  <div class="book-id">
                    ID: {{ bookItem.book?.id ?? '—' }}
                  </div>
                </div>
                <div class="book-status">
                  <span class="status-badge small" :class="getBookStatusClass(bookItem.status)">
                    {{ getBookStatusText(bookItem.status) }}
                  </span>
                </div>
              </div>
            </div>
            <div v-else>
              <p>Книги отсутствуют.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="close-modal-btn" @click="closeModal">
          Закрыть
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import { getOrderDetails } from "@api/orders";
import type { Order } from "@api/types";
import { orderStatuses, orderBookStatuses } from "@api/types";
import type { OrderStatusEnum } from "@api/types";

interface Props {
  orderId?: number;
  isOpen: boolean;
}

interface Emits {
  (e: 'update:isOpen', value: boolean): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const order = ref<Order | null>(null);
const error = ref<string | null>(null);

watch(() => props.isOpen, async (newVal) => {
  if (newVal && props.orderId) {
    order.value = null;
    error.value = null;
    try {
      order.value = await getOrderDetails(props.orderId);
      if (!order.value) {
        error.value = 'Данные заказа не найдены';
      }
    } catch (err) {
      console.error('Ошибка загрузки деталей заказа:', err);
      error.value = 'Не удалось загрузить детали заказа. Попробуйте позже.';
    }
  } else if (!newVal) {
    // при закрытии чистим
    order.value = null;
    error.value = null;
  }
});

const closeModal = () => {
  emit('update:isOpen', false);
  order.value = null;
  error.value = null;
};

const currentStatus = computed(() => {
  if (!order.value?.statuses || order.value.statuses.length === 0) return 'unknown';
  return order.value.statuses[order.value.statuses.length - 1].status ?? 'unknown';
});

const getStatusClass = (status: string) => {
  return `status-${status}`;
};

const getStatusText = (status: unknown) => {
  if (typeof status !== 'string') return String(status ?? '-');
  if (status in orderStatuses) {
    return orderStatuses[status as keyof typeof orderStatuses];
  }
  return status;
};

const getBookStatusClass = (status: string) => {
  return `status-${status}`;
};

const getBookStatusText = (status: unknown) => {
  if (typeof status !== 'string') return String(status ?? '-');
  if (status in orderBookStatuses) {
    return orderBookStatuses[status as keyof typeof orderBookStatuses];
  }
  return status;
};

const formatDateTime = (dateString?: string) => {
  if (!dateString) return '-';
  try {
    return new Date(dateString).toLocaleString('ru-RU');
  } catch {
    return dateString;
  }
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
  padding: 0; /* header/padding handled inside sections */
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
