<template>
  <div v-if="selectedOrder" class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Детали заказа #{{ selectedOrder.id }}</h2>
        <button class="close-button" @click="closeModal">×</button>
      </div>

      <div class="modal-body">
        <div class="section">
          <h3>Заказчик:</h3>
          <span>{{ selectedOrder.user.last_name + " " + selectedOrder.user.first_name }}</span>
        </div>
        <div class="section">
          <h3>Книги ({{ selectedOrder.books.length }})</h3>
          <div class="books-container">
            <template v-for="orderBook in selectedOrder.books" :key="orderBook.id">
              <div
                class="book-card"
                :class="{
                  error: isCheckFailed && !validBooksId.includes(orderBook.id),
                  succes: isCheckFailed && validBooksId.includes(orderBook.id),
                }"
              >
                <ShortBookCard :book="orderBook.book" :truncate="isCheckFailed" />
              </div>
              <div
                class="book-card"
                :class="{
                  error: isCheckFailed && !validBooksId.includes(orderBook.id),
                  succes: isCheckFailed && validBooksId.includes(orderBook.id),
                }"
                v-if="isCheckFailed && !validBooksId.includes(orderBook.id)"
              >
                <div>
                  <label>Причина:</label>
                  <select
                    v-model="unavailableBookReason[orderBook.id]"
                    class="form-select"
                    aria-label="Причина, почему книга не найдена"
                  >
                    <option
                      v-for="reason in unavailableReasons"
                      :key="reason.value"
                      :value="reason.value"
                    >
                      {{ reason.label }}
                    </option>
                  </select>
                </div>
                <div class="comment-card">
                  <label>Комментарий:</label>
                  <textarea
                    v-model="unavailableBookComment[orderBook.id]"
                    placeholder="Введите комментарий..."
                  ></textarea>
                </div>
                <div class="" v-if="unavailableBookReason[orderBook.id] === 'analog'">
                  <label>Аналог:</label>
                  <select
                    v-model="selectedAnalogBookId[orderBook.id]"
                    class="form-select"
                    aria-label="Возможные аналоги"
                  >
                    <option v-for="analog in availableAnalogs" :key="analog.id" :value="analog.id">
                      {{ analog.title }} ({{ analog.author }})
                    </option>
                  </select>
                </div>
              </div>
              <div v-else-if="isCheckFailed"></div>
            </template>
          </div>
        </div>

        <div class="section">
          <h3>История статусов:</h3>
          <ul class="status-list">
            <li v-for="status in selectedOrder.statuses" :key="status.date" class="status-item">
              <span class="status-date">{{ formatDate(status.date) }}</span>
              <span class="status-badge" :class="'status-' + status.status">
                {{ orderStatuses[status.status] }}
              </span>
              <span v-if="status.staff !== null" class="staff-name">
                {{ status.staff?.first_name + " " + status.staff?.last_name }}
              </span>
              <span
                v-if="status.description && status.description !== status.status"
                class="status-description"
              >
                ({{ status.description }})
              </span>
            </li>
          </ul>
        </div>
      </div>

      <div class="modal-footer">
        <StyledButton
          v-if="currentStatus == 'processing'"
          @click="openPrintModal = true"
          theme="primary"
        >
          Печать
        </StyledButton>
        <StyledButton
          v-if="currentStatus == 'processing'"
          @click="openRejectModal = true"
          theme="accent"
        >
          Вернуть в новые
        </StyledButton>
        <StyledButton
          v-if="currentStatus == 'ready'"
          @click="changeToCancelledStatus"
          theme="accent"
        >
          Отменить заказ
        </StyledButton>
        <StyledButton v-if="nextStatus" @click="changeToNextStatus" theme="secondary">
          {{ nextStatusButtonText }}
        </StyledButton>
      </div>
      <button v-if="currentStatus == 'processing'" @click="handleCheckFail">
        Перестраиваем вид для неудачной проверки
      </button>
      <button v-if="currentStatus == 'processing'" @click="openPrintStickerModal = true">
        Печать этикетки
      </button>
    </div>
  </div>
  <OrderRejectModal v-model="openRejectModal" @confirm="handleRejectOrder" />
  <PrintModal v-model="openPrintModal" :order="selectedOrder" />
  <PrintStickerModal v-model="openPrintStickerModal" :order="selectedOrder" />
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import ShortBookCard from "@components/ShortBookCard.vue";
import StyledButton from "@components/StyledButton.vue";
import PrintModal from "@staff/components/PrintModal.vue";
import PrintStickerModal from "@staff/components/PrintStickerModal.vue";
import OrderRejectModal from "@staff/components/OrderRejectModal.vue";
import type { Order, OrderCheckingInfo } from "@api/types";
import type { OrderStatusEnum } from "@api/types";
import { orderStatuses } from "@api/types";

const openPrintModal = ref(false);

const openPrintStickerModal = ref(false);

// Составить список возможных причин отсутствия книг
// В последствии перейдут в модуль администратора
const unavailableReasons = ref([
  { value: "analog", label: "Аналог" },
  { value: "noAvailableCopies", label: "Нет доступных экземпляров" },
  { value: "damaged", label: "Книга испорчена" },
]);

// Нужно будет привязать комментарии и аналоги к книгам из заказа
const unavailableBookReason = ref<Record<number, string>>({});
const unavailableBookComment = ref<Record<number, string>>({});
const selectedAnalogBookId = ref<Record<number, number | null>>({});

// Пока взяты для примера аналогов
// Нужно будет заменить на книги из возможных аналогов
const availableAnalogs = ref([
  { id: 1, title: "Война и мир", author: "Л.Н. Толстой" },
  { id: 2, title: "Преступление и наказание", author: "Ф.М. Достоевский" },
]);

const props = defineProps<{
  order: Order;
}>();

const statusTransitions = {
  new: {
    next: "processing",
    nextButtonText: "Взять в работу",
  },
  processing: {
    next: "ready",
    nextButtonText: "Проверить готовность",
  },
  ready: {
    next: "done",
    nextButtonText: "Выдать заказ",
  },
  done: {
    next: null,
    nextButtonText: "",
  },
  archived: {
    next: null,
    nextButtonText: "",
  },
  cancelled: {
    next: null,
    nextButtonText: "",
  },
  error: {
    next: null,
    nextButtonText: "",
  },
} as const;

const emit = defineEmits<{
  (e: "close"): void;
  (e: "nextOrderStatus", orderId: number, nextStatus: OrderStatusEnum, description: string): void;
  (e: "checkOrder", orderId: number): OrderCheckingInfo;
}>();

const selectedOrder = ref<Order>(props.order);

// Реализовать логику проверки нахождения книги в читательском билете
const isCheckFailed = ref(false);

const validBooksId = ref<number[]>([]);

const handleCheckFail = async () => {
  validBooksId.value = props.order.books.map((book) => book.id).filter((id) => id % 2 === 0);

  isCheckFailed.value = !isCheckFailed.value;
};

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleString("ru-RU");
}

function closeModal() {
  emit("close");
}

// function printSearchList() {
//   const options = {
//     name: "searchList",
//     specs: ["fullscreen=yes", "titlebar=yes", "scrollbars=yes"],
//     styles: [],
//   };
// }

const currentStatus = computed(() => {
  return props.order.statuses[props.order.statuses.length - 1].status;
});

const nextStatus = computed(() => {
  return statusTransitions[currentStatus.value].next;
});

const nextStatusButtonText = computed(() => {
  return statusTransitions[currentStatus.value].nextButtonText;
});

const changeToCancelledStatus = () => {
  emit("nextOrderStatus", selectedOrder.value.id, "cancelled", "cancelled");
  emit("close");
};

const openRejectModal = ref(false);
const handleRejectOrder = (rejectReason: string) => {
  console.log(rejectReason);
  emit("nextOrderStatus", selectedOrder.value.id, "new", rejectReason);
  emit("close");
  openRejectModal.value = false;
};

const changeToNextStatus = () => {
  if (nextStatus.value) {
    emit("nextOrderStatus", selectedOrder.value.id, nextStatus.value, nextStatus.value);
    emit("close");
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: grid;
  place-items: center;
  z-index: 1000;
  padding: 1rem;
}

.some-info {
  background-color: red;
  text-align: center;
  width: 150px;
}

.modal-content {
  background: var(--color-background-50);
  border-radius: 0.5rem;
  width: min(100%, 56rem);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.2);
  border: 1px solid var(--color-text-200);
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--color-text-100);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--color-background-100);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.375rem;
  color: var(--color-text-800);
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text-400);
  padding: 0 0.5rem;
  line-height: 1;
  transition: color 0.2s;
}

.close-button:hover {
  color: var(--color-primary-600);
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex-grow: 1;
}

.section {
  margin-bottom: 1.5rem;
  border-bottom: 3px solid var(--color-text-100);
  padding-bottom: 1rem;
}

.section h3 {
  font-size: 1.125rem;
  color: var(--color-text-700);
  font-weight: 500;
}

.status-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.status-item {
  padding: 0.75rem 0;
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  border-bottom: 1px dashed var(--color-text-100);
}

.status-item:last-child {
  border-bottom: none;
}

.status-date {
  color: var(--color-text-500);
  font-size: 0.875rem;
  min-width: 10rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid transparent;
}

.status-new {
  background-color: var(--background-status-new);
  color: var(--color-status-new);
  border-color: var(--color-status-new);
}

.status-processing {
  background-color: var(--background-status-processing);
  color: var(--color-status-processing);
  border-color: var(--color-status-processing);
}

.status-ready {
  background-color: var(--background-status-ready);
  color: var(--color-status-ready);
  border-color: var(--color-status-ready);
}

.status-done {
  background-color: var(--background-status-done);
  color: var(--color-status-done);
  border-color: var(--color-status-done);
}

.status-cancelled {
  background-color: var(--background-status-cancelled);
  color: var(--color-status-cancelled);
  border-color: var(--color-status-cancelled);
}

.status-error {
  background-color: var(--background-status-error);
  color: var(--color-status-error);
  border-color: var(--color-status-error);
}

.status-archived {
  background-color: var(--background-status-archived);
  color: var(--color-status-archived);
  border-color: var(--color-status-archived);
}

.status-description {
  color: var(--color-text-500);
  font-size: 0.875rem;
  flex-basis: 100%;
  margin-top: 0.25rem;
  padding-left: 11rem;
}

.books-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(18rem, 1fr));
  gap: 1rem;
}

.book-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1rem;
  gap: 0.5rem;
  background-color: var(--color-background-100);
  transition:
    transform 0.2s,
    box-shadow 0.2s;
  &.error {
    background-color: var(--background-status-error);
  }

  &.succes {
    background-color: var(--background-status-done);
  }
}

.book-card:hover {
  transform: translateY(-0.125rem);
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.1);
}

.extend-info {
  padding: 1rem;
  background-color: var(--color-accent-200);
  font-size: 0.875rem;
}

.form-select {
  border: 1px solid var(--color-text-200);
}
.comment-card {
  display: flex;
  flex-direction: column;
}
.comment-card textarea {
  width: 100%;
  min-height: 50px;
  padding: 0.75rem;
  border: 1px solid var(--color-text-200);
  border-radius: 0.5rem;
}

.book-number,
.book-status,
.book-date {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.status-label,
.date-label {
  color: var(--color-text-500);
}

.status-value {
  font-weight: 500;
}

.status-ordered {
  color: var(--color-primary-600);
}
.status-handed {
  color: var(--color-secondary-600);
}
.status-returned {
  color: var(--color-accent-600);
}
.status-cancelled {
  color: var(--color-text-700);
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--color-text-100);
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  background-color: var(--color-background-100);
}

@media (max-width: 640px) {
  .status-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .status-date {
    min-width: auto;
  }

  .status-description {
    padding-left: 0;
  }

  .books-container {
    grid-template-columns: 1fr;
  }

  .modal-footer {
    flex-direction: column;
  }
}
</style>
