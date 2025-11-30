<!-- OrderDetailsModal.vue (updated with optional chaining and error handling) -->
<template>
  <div class="modal" v-if="isOpen">
    <div class="modal-content">
      <h3>Детали заказа #{{ orderId }}</h3>
      <div v-if="error">
        <p>Ошибка загрузки: {{ error }}</p>
      </div>
      <div v-else-if="order">
        <p>ФИО читателя: {{ order.user?.fullname || `${order.user?.first_name || ''} ${order.user?.last_name || ''}` }}</p>
        <p>Статус: {{ orderStatuses[order.statuses[order.statuses.length - 1]?.status] }}</p>
        <!-- Add more details like books, statuses history, etc. -->
        <ul>
          <li v-for="status in order.statuses" :key="status.date">
            {{ status.date }}: {{ orderStatuses[status.status] }} ({{ status.staff?.fullname || 'Неизвестно' }})
          </li>
        </ul>
        <h4>Книги:</h4>
        <ul>
          <li v-for="book in order.books" :key="book.id">
            {{ book.book?.title || 'Без названия' }} - Статус: {{ orderBookStatuses[book.status] }}
          </li>
        </ul>
      </div>
      <div v-else>
        Загрузка...
      </div>
      <button @click="closeModal">Закрыть</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { getOrderDetails } from "@api/orders";
import type { Order } from "@api/types";
import { orderStatuses, orderBookStatuses } from "@api/types";

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
      if (!order.value?.user) {
        error.value = 'Данные пользователя не найдены';
      }
    } catch (err) {
      console.error('Ошибка загрузки деталей заказа:', err);
      error.value = 'Не удалось загрузить детали заказа. Попробуйте позже.';
    }
  }
});

const closeModal = () => {
  emit('update:isOpen', false);
  order.value = null;
  error.value = null;
};
</script>

<style scoped lang="scss">
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 600px;
  overflow: auto;
}
</style>