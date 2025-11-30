<template>
  <div v-if="isOpen" class="modal-overlay" @click="close">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>Заказы читателя</h3>
        <button class="close-btn" @click="close" aria-label="Закрыть">
          &times;
        </button>
      </div>

      <div class="reader-info">
        <div class="reader-info-item">
          <strong>ФИО:</strong> {{ reader.fullname }}
        </div>
        <div class="reader-info-item">
          <strong>Чит. билет:</strong> {{ reader.library_card }}
        </div>
        <div class="reader-info-item">
          <strong>Подразделение:</strong> {{ reader.department }}
        </div>
        <div class="reader-info-item">
          <strong>Всего заказов:</strong> {{ reader.total_orders }}
        </div>
        <div class="reader-info-item">
          <strong>Заказано книг:</strong> {{ reader.total_books_ordered }}
        </div>
        <div class="reader-info-item">
          <strong>Отмененные заказы:</strong> {{ reader.cancelled_orders }}
        </div>
      </div>

      <div class="orders-section">
        <h4>История заказов</h4>
        
        <div v-if="loading" class="loading-state">
          Загрузка заказов...
        </div>
        
        <div v-else class="table-container">
          <table class="orders-table">
            <thead>
              <tr>
                <th>ID заказа</th>
                <th>Библиотека</th>
                <th>Текущий статус</th>
                <th>Дата создания</th>
                <th>Количество книг</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="order in orders" 
                :key="order.id"
                class="order-row"
                @click="showOrderDetails(order)"
              >
                <td>#{{ order.id }}</td>
                <td>{{ order.library.description }}</td>
                <td>
                  <span class="status-badge" :class="getStatusClass(currentStatus(order))">
                    {{ getStatusText(currentStatus(order)) }}
                  </span>
                </td>
                <td>{{ formatDate(order.statuses[0]?.date) }}</td>
                <td>{{ getBooksCount(order) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="!loading && orders.length === 0" class="empty-orders">
          У читателя нет заказов
        </div>
      </div>

      <OrderDetailsModal
        v-if="selectedOrder"
        :order="selectedOrder"
        :reader="reader"
        @close="selectedOrder = null"
      />

      <div class="modal-footer">
        <button class="close-modal-btn" @click="close">
          Закрыть
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onUnmounted, nextTick } from 'vue';
import type { ReaderStats, Order } from "@api/types";
import { orderStatuses } from "@api/types";
import { getReaderOrders, getReaderOrderDetail } from "@api/readers";
import OrderDetailsModal from '@modules/moderator/components/OrderDetailsModal.vue';

interface Props {
  isOpen: boolean;
  reader: ReaderStats;
}

interface Emits {
  (e: 'update:isOpen', value: boolean): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const orders = ref<Order[]>([]);
const loading = ref(false);
const selectedOrder = ref<Order | null>(null);
let abortController: AbortController | null = null;
let isInitialLoad = true;

const close = () => {
  emit('update:isOpen', false);
};

const currentStatus = (order: Order): string => {
  if (!order.statuses || order.statuses.length === 0) return 'unknown';
  return order.statuses[order.statuses.length - 1].status;
};

const getStatusClass = (status: string) => {
  return `status-${status}`;
};

const getStatusText = (status: string) => {
  return orderStatuses[status as keyof typeof orderStatuses] || status;
};

const getBooksCount = (order: Order): number => {
  return order.books?.length || 0;  
};

const formatDate = (dateString: string | undefined) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString('ru-RU');
};

const loadReaderOrders = async () => {
  if (!props.reader) return;
  
  if (abortController) {
    abortController.abort();
  }
  
  abortController = new AbortController();
  loading.value = true;
  
  try {
    const readerOrders = await getReaderOrders(props.reader.id);
    orders.value = readerOrders;
  } catch (error: any) {
    if (error.name !== 'AbortError') {
      console.error('Ошибка загрузки заказов читателя:', error);
    }
  } finally {
    loading.value = false;
    abortController = null;
  }
};

const showOrderDetails = async (order: Order) => {
  try {
    const orderDetail = await getReaderOrderDetail(props.reader.id, order.id);
    selectedOrder.value = orderDetail;
  } catch (error) {
    console.error('Ошибка загрузки деталей заказа:', error);
  }
};

watch(() => props.isOpen, async (isOpen) => {
  if (isOpen && props.reader) {
    await nextTick();
    
    if (isInitialLoad || orders.value.length === 0) {
      await loadReaderOrders();
      isInitialLoad = false;
    }
  } else {
    orders.value = [];
    selectedOrder.value = null;
    isInitialLoad = true;
  }
}, { immediate: true });

onUnmounted(() => {
  if (abortController) {
    abortController.abort();
  }
});
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
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 1000px;
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
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:hover {
    color: var(--color-text-800);
    background: var(--color-background-200);
    border-radius: 4px;
  }
}

.reader-info {
  padding: 1.5rem;
  background: var(--color-background-100);
  border-bottom: 1px solid var(--color-text-200);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  
  .reader-info-item {
    strong {
      color: var(--color-text-700);
      display: block;
      margin-bottom: 0.25rem;
      font-size: 0.875rem;
    }
  }
}

.orders-section {
  padding: 1.5rem;
  
  h4 {
    margin: 0 0 1rem 0;
    color: var(--color-text-800);
  }
}

.loading-state {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-600);
}

.table-container {
  overflow-x: auto;
  border: 1px solid var(--color-text-200);
  border-radius: 4px;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
  
  th, td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--color-text-200);
  }
  
  th {
    background: var(--color-background-200);
    color: var(--color-text-700);
    font-weight: 600;
    font-size: 0.875rem;
    white-space: nowrap;
  }
  
  td {
    background: white;
    color: var(--color-text-800);
  }
  
  tr:last-child td {
    border-bottom: none;
  }
}

.order-row {
  cursor: pointer;
  transition: background-color 0.2s;
  
  &:hover {
    background-color: var(--color-background-100);
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
  
  &.status-unknown {
    background: var(--color-text-100);
    color: var(--color-text-600);
  }
}

.empty-orders {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-600);
  font-style: italic;
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