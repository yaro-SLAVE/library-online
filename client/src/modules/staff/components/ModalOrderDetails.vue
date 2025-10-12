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
                v-if="
                  isCheckFailed &&
                  !validBooksId.includes(orderBook.id) &&
                  unavailableBooks.includes(orderBook.id)
                "
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
                      :label="reason.label"
                    />
                  </select>
                </div>
                <div class="comment-card">
                  <label>Комментарий:</label>
                  <textarea
                    v-model="unavailableBookComment[orderBook.id]"
                    placeholder="Введите комментарий..."
                  ></textarea>
                </div>
                <div
                  v-if="
                    unavailableBookReason[orderBook.id] === 'analogous' &&
                    unavailableBooks.includes(orderBook.id)
                  "
                >
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
          @click="openCancelModal = true"
          theme="accent"
        >
          Отменить заказ
        </StyledButton>
        <StyledButton
          v-if="currentStatus == 'processing' && isCheckFailed !== true"
          @click="checkOrderAvailability"
          theme="secondary"
        >
          {{ nextStatusButtonText }}
        </StyledButton>
        <StyledButton
          v-if="currentStatus == 'processing' && isCheckFailed === true"
          @click="checkOrderAvailability"
          theme="secondary"
        >
          Повторно првоерить готовность
        </StyledButton>
        <StyledButton
          v-if="nextStatus && currentStatus !== 'processing'"
          @click="changeToNextStatus"
          theme="secondary"
        >
          {{ nextStatusButtonText }}
        </StyledButton>
      </div>
      <!-- <button v-if="currentStatus == 'processing'" @click="checkOrderAvailability">
        Перестраиваем вид для неудачной проверки
      </button> -->
      <button v-if="currentStatus == 'processing'" @click="openPrintStickerModal = true">
        Печать этикетки
      </button>
    </div>
  </div>
  <OrderRejectModal v-model="openRejectModal" @confirm="handleRejectOrder" />
  <OrderCancelModal v-model="openCancelModal" @confirm="handleOrderCancel" />
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
import OrderCancelModal from "@staff/components/OrderCancelModal.vue";

const openPrintModal = ref(false);
const openPrintStickerModal = ref(false);

const openCancelModal = ref(false);

const handleOrderCancel = (cancelData: { reason: string; comment: string }) => {
  // Формируем описание для статуса
  const reasonLabel =
    cancellationReasons.value.find((r) => r.value === cancelData.reason)?.label || "";
  const description = `${reasonLabel}${cancelData.comment ? `: ${cancelData.comment}` : ""}`;

  emit("nextOrderStatus", selectedOrder.value.id, "cancelled", description);
  openCancelModal.value = false;
  emit("close");
};

const cancellationReasons = ref([
  { value: "debt", label: "Не принес долги" },
  { value: "no_show", label: "В черном списке" },
  { value: "changed_mind", label: "Должник по учебе" },
]);

const props = defineProps<{
  order: Order;
  onCheckOrder: (orderId: number) => Promise<OrderCheckingInfo | undefined>;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "nextOrderStatus", orderId: number, nextStatus: OrderStatusEnum, description: string): void;
}>();

const selectedOrder = ref<Order>(props.order);

const unavailableReasons = ref([
  { value: "noAvailableCopies", label: "Нет доступных экземпляров" },
  { value: "damaged", label: "Книга испорчена" },
]);

const unavailableBookReason = ref<Record<number, string>>({});
const unavailableBookComment = ref<Record<number, string>>({});
const selectedAnalogBookId = ref<Record<number, number | null>>({});

const validBooksId = ref<number[]>([]);
const unavailableBooks = ref<number[]>([]);
const availableAnalogs = ref<{ id: number; title: string; author: string }[]>([]);

const isCheckFailed = ref(false);

const checkOrderAvailability = async () => {
  try {
    const result = await props.onCheckOrder(selectedOrder.value.id);
    console.log("Результат проверки заказа:", result);

    if (!result) {
      console.error("Не удалось получить результат проверки");
      return;
    }

    if (result) {
      // Разбиваем результат на 3 отдельных массива
      const foundBooks = result.found_books || [];
      const notFoundBooks = result.notfound_books || [];
      const additionalBooks = result.additional_books || [];

      console.log("Найденные книги:", foundBooks);
      console.log("Ненайденные книги:", notFoundBooks);
      console.log("Аналоги:", additionalBooks);

      validBooksId.value = foundBooks.map((book) => book.id);
      unavailableBooks.value = notFoundBooks.map((book) => book.id);
      availableAnalogs.value = additionalBooks;

      if (availableAnalogs.value.length > 0) {
        unavailableReasons.value.push({ value: "analogous", label: "Аналог" });
      }

      // notFoundBooks.forEach(book => {
      //   unavailableBookReason.value[book.id] = '';
      //   unavailableBookComment.value[book.id] = '';
      //   selectedAnalogBookId.value[book.id] = null;
      // });

      if (notFoundBooks.length > 0 && !validateNotFoundBooks()) {
        isCheckFailed.value = true;
      } else {
        if (validateNotFoundBooks()) {
          console.log("Все причины и аналоги заполнены");

          const updates = unavailableBooks.value.map((bookId) => ({
            book_id: bookId,
            description:
              unavailableBookReason.value[bookId] !== null
                ? unavailableBookReason.value[bookId]
                : unavailableBookComment.value[bookId] !== null
                  ? unavailableBookComment.value[bookId]
                  : "",
            status: unavailableBookReason.value[bookId] === "analogous" ? "analogous" : "cancelled",
            analogous:
              unavailableBookReason.value[bookId] === "analogous"
                ? selectedAnalogBookId.value[bookId]
                : "",
          }));
          console.log("Данные для отправки на бэк:", updates);

          if (nextStatus.value)
            emit(
              "nextOrderStatus",
              selectedOrder.value.id,
              nextStatus.value,
              nextStatus.value,
              updates
            );
          emit("close");
        }
      }
    } else {
      console.error("Не удалось получить результат проверки");
    }
  } catch (error) {
    console.error("Ошибка при вызове проверки заказа:", error);
  }
};

const validateNotFoundBooks = (): boolean => {
  return unavailableBooks.value.every((bookId) => {
    const reason = unavailableBookReason.value[bookId];
    // Проверяем что указана причина
    if (!reason) {
      console.log(`Для книги ID:${bookId} не указана причина`);
      return false;
    }
    // Если причина "analog", проверяем что выбран аналог
    if (reason === "analogous") {
      const analogId = selectedAnalogBookId.value[bookId];
      if (!analogId) {
        console.warn(`Для книги ID:${bookId} не выбран аналог`);
        return false;
      }
    }
    return true;
  });
};

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
