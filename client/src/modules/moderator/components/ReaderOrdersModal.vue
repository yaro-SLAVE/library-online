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
          <strong>Институт:</strong> {{ reader.department }}
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
        
        <div class="table-container">
          <table class="orders-table">
            <thead>
              <tr>
                <th>№ заказа</th>
                <th>Итоговый статус</th>
                <th>Дата и время создания</th>
                <th>Собран</th>
                <th>Готов к выдаче</th>
                <th>Выдан</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id">
                <td>{{ order.id }}</td>
                <td>
                  <span class="status-badge" :class="getStatusClass(order.final_status)">
                    {{ getStatusText(order.final_status) }}
                  </span>
                </td>
                <td>{{ formatDateTime(order.created_at) }}</td>
                <td>{{ formatDateTime(order.collected_at) }}</td>
                <td>{{ formatDateTime(order.ready_at) }}</td>
                <td>{{ formatDateTime(order.issued_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="orders.length === 0" class="empty-orders">
          Нет данных о заказах
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
import { ref, watch } from 'vue';
import type { ReaderStats } from "@api/types";

interface Order {
  id: number;
  final_status: string;
  created_at: string;
  collected_at: string | null;
  ready_at: string | null;
  issued_at: string | null;
}

interface Props {
  isOpen: boolean;
  reader: ReaderStats | null;
}

interface Emits {
  (e: 'update:isOpen', value: boolean): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const orders = ref<Order[]>([]);
const loading = ref(false);

const close = () => {
  emit('update:isOpen', false);
};

const getStatusClass = (status: string) => {
  const statusMap: { [key: string]: string } = {
    'created': 'status-created',
    'collected': 'status-collected',
    'ready': 'status-ready',
    'issued': 'status-issued',
    'cancelled': 'status-cancelled'
  };
  return statusMap[status] || 'status-unknown';
};

const getStatusText = (status: string) => {
  const statusMap: { [key: string]: string } = {
    'created': 'Создан',
    'collected': 'Собран',
    'ready': 'Готов к выдаче',
    'issued': 'Выдан',
    'cancelled': 'Отменен'
  };
  return statusMap[status] || status;
};

const formatDateTime = (dateTime: string | null) => {
  if (!dateTime) return '-';
  return new Date(dateTime).toLocaleString('ru-RU');
};

// Заглушка данных для демонстрации
const generateMockOrders = (readerId: number): Order[] => {
  const baseDate = new Date('2024-01-15');
  const statuses = ['created', 'collected', 'ready', 'issued', 'cancelled'];
  
  return Array.from({ length: 8 }, (_, index) => {
    const status = statuses[index % statuses.length];
    const orderDate = new Date(baseDate);
    orderDate.setDate(orderDate.getDate() + index);
    
    return {
      id: readerId * 1000 + index + 1,
      final_status: status,
      created_at: new Date(orderDate.setHours(10, 0, 0)).toISOString(),
      collected_at: status !== 'created' && status !== 'cancelled' 
        ? new Date(orderDate.setHours(11, 0, 0)).toISOString() 
        : null,
      ready_at: status === 'ready' || status === 'issued' 
        ? new Date(orderDate.setHours(11, 30, 0)).toISOString() 
        : null,
      issued_at: status === 'issued' 
        ? new Date(orderDate.setHours(12, 0, 0)).toISOString() 
        : null
    };
  });
};

// Загрузка заглушечных данных при открытии модального окна
watch(() => props.isOpen, (isOpen) => {
  if (isOpen && props.reader) {
    loading.value = true;
    // Имитация загрузки данных
    setTimeout(() => {
      orders.value = generateMockOrders(props.reader!.id);
      loading.value = false;
    }, 300);
  } else {
    orders.value = [];
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
  max-width: 1200px;
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
    
    &:last-child {
      margin-bottom: 0;
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

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
  
  &.status-created {
    background: var(--color-info-100);
    color: var(--color-info-700);
  }
  
  &.status-collected {
    background: var(--color-warning-100);
    color: var(--color-warning-700);
  }
  
  &.status-ready {
    background: var(--color-success-100);
    color: var(--color-success-700);
  }
  
  &.status-issued {
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