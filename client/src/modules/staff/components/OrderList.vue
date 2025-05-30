<template>
  <div class="table-container">
    <table class="table">
      <thead>
        <tr>
          <th
            @click="resetSorting"
            class="sortable-th"
            :aria-sort="sortKey === 'id' ? (sortOrder === 1 ? 'ascending' : 'descending') : 'none'"
          >
            <span class="th-content">
              #
              <div class="th-icon">
                <span v-if="sortKey === 'id'" class="direction-icon">
                  {{ sortOrder === 1 ? "↑" : "↓" }}
                </span>
                <span v-else>⇅</span>
              </div>
            </span>
          </th>
          <th
            @click="sortOrders('user')"
            class="sortable-th"
            :aria-sort="
              sortKey === 'user' ? (sortOrder === 1 ? 'ascending' : 'descending') : 'none'
            "
          >
            <span class="th-content">
              Клиент
              <div class="th-icon">
                <span v-if="sortKey === 'user'" class="direction-icon">
                  {{ sortOrder === 1 ? "↑" : "↓" }}
                </span>
                <span v-else>⇅</span>
              </div>
            </span>
          </th>
          <th
            @click="sortOrders('date')"
            class="sortable-th"
            :aria-sort="
              sortKey === 'date' ? (sortOrder === 1 ? 'ascending' : 'descending') : 'none'
            "
          >
            <span class="th-content">
              Дата и время
              <span class="th-icon">
                <span v-if="sortKey === 'date'" class="direction-icon">
                  {{ sortOrder === 1 ? "↑" : "↓" }}
                </span>
                <span v-else>⇅</span>
              </span>
            </span>
          </th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in sortedOrders" :key="order.id">
          <th>{{ order.id }}</th>
          <td>{{ order.user.first_name }} {{ order.user.last_name }}</td>
          <td>{{ formatDate(order.statuses[0]?.date) }}</td>
          <td>
            <button
              class="info-button"
              @click="handleOpenOrderDetails(order.id)"
              aria-label="Показать детали заказа"
            >
              Инфо
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref, computed } from "vue";
import type { UserOrder } from "@api/types";

const props = defineProps<{
  orders: UserOrder[];
}>();

const emit = defineEmits<{
  (e: "getOrder", id: number): void;
}>();

type SortKey = "id" | "user" | "date";

const sortKey = ref<SortKey>("id");
const sortOrder = ref<1 | -1>(1);

function formatDate(dateString?: string): string {
  if (!dateString) return "---";

  try {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("ru-RU", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
    })
      .format(date)
      .replace(",", " |");
  } catch {
    return dateString;
  }
}

function resetSorting() {
  sortKey.value = "id";
  sortOrder.value = 1;
}

function sortOrders(key: SortKey) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 1 ? -1 : 1;
  } else {
    sortKey.value = key;
    sortOrder.value = 1;
  }
}

const sortedOrders = computed(() => {
  if (!props.orders) return [];

  return [...props.orders].sort((a, b) => {
    let comparison = 0;

    switch (sortKey.value) {
      case "user":
        const aUser = `${a.user.first_name} ${a.user.last_name}`.toLowerCase();
        const bUser = `${b.user.first_name} ${b.user.last_name}`.toLowerCase();
        comparison = aUser.localeCompare(bUser);
        break;
      case "date":
        const aDate = a.statuses[0]?.date ? new Date(a.statuses[0].date).getTime() : 0;
        const bDate = b.statuses[0]?.date ? new Date(b.statuses[0].date).getTime() : 0;
        comparison = aDate - bDate;
        break;
      case "id":
      default:
        comparison = a.id - b.id;
    }

    return comparison * sortOrder.value;
  });
});

const handleOpenOrderDetails = (orderId: number) => {
  emit("getOrder", orderId);
};
</script>

<style scoped lang="scss">
.table-container {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 12px;
  text-align: left;
  color: var(--color-text-800);
  background-color: var(--color-background-100);
}

tr {
  border-bottom: 1px solid var(--color-text-200);
}

.sortable-th {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;

  &:hover {
    background-color: var(--color-background-200);

    .th-icon {
      opacity: 1;
    }
  }

  &[aria-sort="ascending"],
  &[aria-sort="descending"] {
    .th-icon {
      opacity: 1;
      font-weight: bold;
    }
  }
}

.th-content {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.th-icon {
  font-size: 0.9em;
  opacity: 0.7;
  transition: opacity 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1em;
  height: 1em;
}

.direction-icon {
  font-weight: bold;
  color: var(--color-primary-500);
}

.info-button {
  padding: 6px 12px;
  border: none;
  font-size: 14px;
  border-radius: 5px;
  cursor: pointer;
  background-color: var(--color-primary-400);
  transition: background-color 0.2s;

  &:hover {
    background-color: var(--color-accent-700);
  }

  &:focus-visible {
    outline: 2px solid var(--color-accent-500);
    outline-offset: 2px;
  }
}
</style>
