<template>
  <div class="table-container">
    <table class="table">
      <thead>
        <tr>
          <th
            @click="sortCandidates('library_card')"
            class="sortable-th library-card-column"
            :aria-sort="sortKey === 'library_card' ? (sortOrder === 1 ? 'ascending' : 'descending') : 'none'"
          >
            <span class="th-content">
              Читательский билет
              <div class="th-icon">
                <span v-if="sortKey === 'library_card'" class="direction-icon">
                  {{ sortOrder === 1 ? "↑" : "↓" }}
                </span>
                <span v-else>⇅</span>
              </div>
            </span>
          </th>
          <th
            @click="sortCandidates('fullname')"
            class="sortable-th fullname-column"
            :aria-sort="sortKey === 'fullname' ? (sortOrder === 1 ? 'ascending' : 'descending') : 'none'"
          >
            <span class="th-content">
              ФИО
              <div class="th-icon">
                <span v-if="sortKey === 'fullname'" class="direction-icon">
                  {{ sortOrder === 1 ? "↑" : "↓" }}
                </span>
                <span v-else>⇅</span>
              </div>
            </span>
          </th>
          
          <th 
            @click="sortCandidates('is_candidate')"
            class="sortable-th candidate-column"
            :aria-sort="sortKey === 'is_candidate' ? (sortOrder === 1 ? 'ascending' : 'descending') : 'none'"
          >
            <span class="th-content">
              Претендент на блокировку
              <div class="th-icon">
                <span v-if="sortKey === 'is_candidate'" class="direction-icon">
                  {{ sortOrder === 1 ? "↑" : "↓" }}
                </span>
                <span v-else>⇅</span>
              </div>
            </span>
          </th>

          <th
            @click="sortCandidates('total_orders_count')"
            class="sortable-th orders-column"
            :aria-sort="sortKey === 'total_orders_count' ? (sortOrder === 1 ? 'ascending' : 'descending') : 'none'"
          >
            <span class="th-content">
              Количество заказов
              <div class="th-icon">
                <span v-if="sortKey === 'total_orders_count'" class="direction-icon">
                  {{ sortOrder === 1 ? "↑" : "↓" }}
                </span>
                <span v-else>⇅</span>
              </div>
            </span>
          </th>
          <th
            @click="sortCandidates('cancelled_orders_count')"
            class="sortable-th cancellations-column"
            :aria-sort="sortKey === 'cancelled_orders_count' ? (sortOrder === 1 ? 'ascending' : 'descending') : 'none'"
          >
            <span class="th-content">
              Количество отказов
              <div class="th-icon">
                <span v-if="sortKey === 'cancelled_orders_count'" class="direction-icon">
                  {{ sortOrder === 1 ? "↑" : "↓" }}
                </span>
                <span v-else>⇅</span>
              </div>
            </span>
          </th>
          <th class="actions-column">Действия</th>
        </tr>
      </thead>
      <tbody>
        <BanCandidatesTableRow
          v-for="candidate in sortedCandidates"
          :key="candidate.user_id"
          :candidate="candidate"
          @ban-user="handleBanUser"
          :loading="loadingBanId === candidate.user_id"
        />
      </tbody>
    </table>
    <div v-if="candidates.length === 0 && !loading" class="empty-state">
      {{ hasSearched ? 'Кандидаты на блокировку не найдены' : 'Укажите период для поиска кандидатов' }}
    </div>
    <div v-if="loading" class="loading-state">
      Загрузка...
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import type { BanCandidate } from "@api/profile";
import BanCandidatesTableRow from "@moderator/components/BanCandidatesTableRow.vue";

const props = defineProps<{
  candidates: BanCandidate[];
  loading: boolean;
  loadingBanId?: number | null;
  hasSearched: boolean;
}>();

const emit = defineEmits<{
  (e: "banUser", userId: number): void;
}>();

// Добавили "is_candidate" в типы ключей сортировки
type SortKey = "library_card" | "fullname" | "total_orders_count" | "cancelled_orders_count" | "is_candidate";

const sortKey = ref<SortKey>("cancelled_orders_count");
const sortOrder = ref<1 | -1>(-1); 

function sortCandidates(key: SortKey) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 1 ? -1 : 1;
  } else {
    sortKey.value = key;
    sortOrder.value = 1;
  }
}

const sortedCandidates = computed(() => {
  if (!props.candidates) return [];

  return [...props.candidates].sort((a, b) => {
    let comparison = 0;

    switch (sortKey.value) {
      case "fullname":
        comparison = (a.fullname || '').localeCompare(b.fullname || '');
        break;
      case "is_candidate":
        // Сортировка "Да"/"Нет"
        comparison = (a.is_candidate || '').localeCompare(b.is_candidate || '');
        break;
      case "total_orders_count":
        comparison = a.total_orders_count - b.total_orders_count;
        break;
      case "cancelled_orders_count":
        comparison = a.cancelled_orders_count - b.cancelled_orders_count;
        break;
      case "library_card":
      default:
        comparison = (a.library_card || '').localeCompare(b.library_card || '');
    }

    return comparison * sortOrder.value;
  });
});

const handleBanUser = (userId: number) => {
  emit("banUser", userId);
};
</script>

<style scoped lang="scss">
.table-container {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  min-width: 320px;
  background-color: var(--color-background-100);
}

th,
td {
  padding: 12px 8px;
  text-align: left;
  color: var(--color-text-800);
  background-color: var(--color-background-100);
  
  @media (max-width: 768px) {
    padding: 10px 6px;
    font-size: 0.9em;
  }
  
  @media (max-width: 480px) {
    padding: 8px 4px;
    font-size: 0.85em;
  }
}

tr {
  border-bottom: 1px solid var(--color-text-200);
}

.library-card-column {
  width: 15%;
  min-width: 100px;
}

.fullname-column {
  width: 25%;
  min-width: 120px;
}

.candidate-column {
  width: 15%;
  min-width: 120px;
  font-weight: 500;
}

.orders-column,
.cancellations-column {
  width: 12%;
  min-width: 100px;
}

.actions-column {
  width: 15%;
  min-width: 100px;
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
  white-space: nowrap;
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

.empty-state,
.loading-state {
  text-align: center;
  padding: 40px;
  color: var(--color-text-600);
  font-size: 1.1em;
  background-color: var(--color-background-100);
}
</style>