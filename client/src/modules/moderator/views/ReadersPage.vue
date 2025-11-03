<template>
  <div class="readers-page">
    <div class="page-header">
      <h2>Читатели</h2>
      <div class="stats">
        Всего читателей: {{ pagination.total }}
      </div>
    </div>

    <div v-if="dateError" class="error-message">
      {{ dateError }}
    </div>

    <div class="filters-section">
      <div class="filters-grid">
        <div class="filter-group">
          <label for="fullname-filter" class="filter-label">ФИО</label>
          <input 
            id="fullname-filter"
            v-model="localFilters.fullname" 
            type="text" 
            placeholder="Поиск по ФИО..."
            class="filter-input"
            :disabled="loading"
          >
        </div>

        <div class="filter-group">
          <label for="department-filter" class="filter-label">Институт</label>
          <input 
            id="department-filter"
            v-model="localFilters.department" 
            type="text" 
            placeholder="Поиск по институту..."
            class="filter-input"
            :disabled="loading"
          >
        </div>

        <div class="filter-group">
          <label class="filter-label">Дата регистрации</label>
          <div class="date-inputs">
            <input 
              v-model="localFilters.registrationDateFrom" 
              type="date" 
              class="filter-input date"
              :disabled="loading"
              placeholder="От"
            >
            <span class="date-separator">—</span>
            <input 
              v-model="localFilters.registrationDateTo" 
              type="date" 
              class="filter-input date"
              :disabled="loading"
              placeholder="До"
            >
          </div>
        </div>

        <div class="filter-group">
          <label class="filter-label">Дата заказа</label>
          <div class="date-inputs">
            <input 
              v-model="localFilters.lastOrderDateFrom" 
              type="date" 
              class="filter-input date"
              :disabled="loading"
              placeholder="От"
            >
            <span class="date-separator">—</span>
            <input 
              v-model="localFilters.lastOrderDateTo" 
              type="date" 
              class="filter-input date"
              :disabled="loading"
              placeholder="До"
            >
          </div>
        </div>

        <div class="filter-actions">
          <button 
            @click="applyFilters" 
            class="apply-filters-btn"
            type="button"
            :disabled="loading || !hasFilterChanges"
          >
            Применить
          </button>
          <button 
            v-if="hasActiveFilters"
            @click="clearAllFilters" 
            class="clear-filters-btn"
            type="button"
            :disabled="loading"
          >
            Сбросить
          </button>
        </div>
      </div>
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th
              @click="resetSorting"
              class="sortable-th"
              :class="{ 
                'active-sort': sortField === 'id', 
                'sort-loading': loading,
                'sort-asc': sortField === 'id' && sortDirection === 'asc',
                'sort-desc': sortField === 'id' && sortDirection === 'desc'
              }"
              :aria-sort="sortField === 'id' ? (sortDirection === 'asc' ? 'ascending' : 'descending') : 'none'"
              role="columnheader"
              tabindex="0"
              @keydown.enter="resetSorting"
              @keydown.space.prevent="resetSorting"
            >
              <span class="th-content">
                #
                <span class="th-icon">
                  <span v-if="sortField === 'id'" class="direction-icon">
                    {{ sortDirection === 'asc' ? "↓" : "↑" }}
                  </span>
                  <span v-else>⇅</span>
                </span>
              </span>
            </th>
            <th
              @click="sortBy('fullname')"
              class="sortable-th"
              :class="{ 
                'active-sort': sortField === 'fullname', 
                'sort-loading': loading,
                'sort-asc': sortField === 'fullname' && sortDirection === 'asc',
                'sort-desc': sortField === 'fullname' && sortDirection === 'desc'
              }"
              :aria-sort="sortField === 'fullname' ? (sortDirection === 'asc' ? 'ascending' : 'descending') : 'none'"
              role="columnheader"
              tabindex="0"
              @keydown.enter="sortBy('fullname')"
              @keydown.space.prevent="sortBy('fullname')"
            >
              <span class="th-content">
                ФИО читателя
                <span class="th-icon">
                  <span v-if="sortField === 'fullname'" class="direction-icon">
                    {{ sortDirection === 'asc' ? "↓" : "↑" }}
                  </span>
                  <span v-else>⇅</span>
                </span>
              </span>
            </th>
            <th role="columnheader" :class="{ 'sort-loading': loading }">
              <span class="th-content">
                Институт
              </span>
            </th>
            <th
              @click="sortBy('total_books_ordered')"
              class="sortable-th"
              :class="{ 
                'active-sort': sortField === 'total_books_ordered', 
                'sort-loading': loading,
                'sort-asc': sortField === 'total_books_ordered' && sortDirection === 'asc',
                'sort-desc': sortField === 'total_books_ordered' && sortDirection === 'desc'
              }"
              :aria-sort="sortField === 'total_books_ordered' ? (sortDirection === 'asc' ? 'ascending' : 'descending') : 'none'"
              role="columnheader"
              tabindex="0"
              @keydown.enter="sortBy('total_books_ordered')"
              @keydown.space.prevent="sortBy('total_books_ordered')"
            >
              <span class="th-content">
                Количество заказанных книг
                <span class="th-icon">
                  <span v-if="sortField === 'total_books_ordered'" class="direction-icon">
                    {{ sortDirection === 'asc' ? "↓" : "↑" }}
                  </span>
                  <span v-else>⇅</span>
                </span>
              </span>
            </th>
            <th
              @click="sortBy('total_orders')"
              class="sortable-th"
              :class="{ 
                'active-sort': sortField === 'total_orders', 
                'sort-loading': loading,
                'sort-asc': sortField === 'total_orders' && sortDirection === 'asc',
                'sort-desc': sortField === 'total_orders' && sortDirection === 'desc'
              }"
              :aria-sort="sortField === 'total_orders' ? (sortDirection === 'asc' ? 'ascending' : 'descending') : 'none'"
              role="columnheader"
              tabindex="0"
              @keydown.enter="sortBy('total_orders')"
              @keydown.space.prevent="sortBy('total_orders')"
            >
              <span class="th-content">
                Количество заказов
                <span class="th-icon">
                  <span v-if="sortField === 'total_orders'" class="direction-icon">
                    {{ sortDirection === 'asc' ? "↓" : "↑" }}
                  </span>
                  <span v-else>⇅</span>
                </span>
              </span>
            </th>
            <th
              @click="sortBy('cancelled_orders')"
              class="sortable-th"
              :class="{ 
                'active-sort': sortField === 'cancelled_orders', 
                'sort-loading': loading,
                'sort-asc': sortField === 'cancelled_orders' && sortDirection === 'asc',
                'sort-desc': sortField === 'cancelled_orders' && sortDirection === 'desc'
              }"
              :aria-sort="sortField === 'cancelled_orders' ? (sortDirection === 'asc' ? 'ascending' : 'descending') : 'none'"
              role="columnheader"
              tabindex="0"
              @keydown.enter="sortBy('cancelled_orders')"
              @keydown.space.prevent="sortBy('cancelled_orders')"
            >
              <span class="th-content">
                Количество отмененных заказов
                <span class="th-icon">
                  <span v-if="sortField === 'cancelled_orders'" class="direction-icon">
                    {{ sortDirection === 'asc' ? "↓" : "↑" }}
                  </span>
                  <span v-else>⇅</span>
                </span>
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <ReadersTableRow 
            v-for="reader in readersData" 
            :key="reader.id" 
            :reader="reader" 
          />
        </tbody>
      </table>

      <div v-if="readersData.length > 0" class="pagination">
        <button 
          @click="prevPage" 
          :disabled="pagination.page === 1 || loading"
          class="pagination-btn"
          type="button"
          aria-label="Предыдущая страница"
        >
          Назад
        </button>
        <span class="pagination-info">
          Страница {{ pagination.page }} из {{ totalPages }}
        </span>
        <button 
          @click="nextPage" 
          :disabled="pagination.page >= totalPages || loading"
          class="pagination-btn"
          type="button"
          aria-label="Следующая страница"
        >
          Вперед
        </button>
      </div>

      <div v-if="readersData.length === 0 && !loading" class="empty-state">
        <div v-if="hasActiveFilters" class="empty-state-content">
          <p>Нет читателей, соответствующих фильтрам</p>
          <button 
            @click="clearAllFilters" 
            class="clear-filters-btn"
            type="button"
            :disabled="loading"
          >
            Сбросить фильтры
          </button>
        </div>
        <div v-else class="empty-state-content">
          <p>Нет данных о читателях</p>
        </div>
      </div>
    </div>

    <LoadingModal v-model="loading" />
  </div>
</template>

<script setup lang="ts">
import ReadersTableRow from "@modules/moderator/components/ReadersTableRow.vue";
import LoadingModal from "@components/LoadingModal.vue";

import { ref, onMounted, onUnmounted, computed, watch } from "vue";
import { useAuthentication } from "@core/composables/auth";
import { useRouter } from "vue-router";
import { getReaders } from "@api/readers";
import type { ReaderStats, ReadersFilters } from "@api/types";

const readersData = ref<ReaderStats[]>([]);
const loading = ref(false);
const router = useRouter();
const dateError = ref('');

const localFilters = ref({
  fullname: '',
  department: '',
  registrationDateFrom: '',
  registrationDateTo: '',
  lastOrderDateFrom: '',
  lastOrderDateTo: '',
});

const activeFilters = ref({
  fullname: '',
  department: '',
  registrationDateFrom: '',
  registrationDateTo: '',
  lastOrderDateFrom: '',
  lastOrderDateTo: '',
});

const pagination = ref({
  page: 1,
  limit: 20,
  total: 0
});

type SortField = 'id' | 'fullname' | 'department' | 'total_books_ordered' | 'total_orders' | 'cancelled_orders';

const sortField = ref<SortField>('id');
const sortDirection = ref<'asc' | 'desc'>('asc');

let abortController: AbortController | null = null;

const hasFilterChanges = computed(() => {
  return JSON.stringify(localFilters.value) !== JSON.stringify(activeFilters.value);
});

const hasActiveFilters = computed(() => {
  const f = activeFilters.value;
  return f.fullname !== '' || f.department !== '' || 
         f.registrationDateFrom !== '' || f.registrationDateTo !== '' ||
         f.lastOrderDateFrom !== '' || f.lastOrderDateTo !== '';
});

const totalPages = computed(() => 
  Math.ceil(pagination.value.total / pagination.value.limit)
);

const requestParams = computed((): ReadersFilters => {
  const params: ReadersFilters = {
    page: pagination.value.page,
    page_size: pagination.value.limit
  };
  
  // Используем активные фильтры, а не локальные
  if (activeFilters.value.fullname) params.fullname = activeFilters.value.fullname;
  if (activeFilters.value.department) params.department = activeFilters.value.department;
  if (activeFilters.value.registrationDateFrom) params.registration_date_from = activeFilters.value.registrationDateFrom;
  if (activeFilters.value.registrationDateTo) params.registration_date_to = activeFilters.value.registrationDateTo;
  if (activeFilters.value.lastOrderDateFrom) params.last_order_date_from = activeFilters.value.lastOrderDateFrom;
  if (activeFilters.value.lastOrderDateTo) params.last_order_date_to = activeFilters.value.lastOrderDateTo;
  
  // Сортировка
  if (sortField.value) {
    params.sort_by = sortField.value;
    params.sort_order = sortDirection.value;
  }
  
  return params;
});

const validateDates = (): boolean => {
  dateError.value = '';
  
  if (!validateDateRange(localFilters.value.registrationDateFrom, localFilters.value.registrationDateTo)) {
    dateError.value = 'Дата начала регистрации не может быть больше даты окончания';
    return false;
  }
  
  if (!validateDateRange(localFilters.value.lastOrderDateFrom, localFilters.value.lastOrderDateTo)) {
    dateError.value = 'Дата начала последнего заказа не может быть больше даты окончания';
    return false;
  }
  
  return true;
};

const validateDateRange = (from: string, to: string): boolean => {
  if (from && to) {
    return new Date(from) <= new Date(to);
  }
  return true;
};

const loadReadersData = async () => {
  if (!validateDates()) return;
  
  // Отменяем предыдущий запрос
  if (abortController) {
    abortController.abort();
  }
  
  abortController = new AbortController();
  loading.value = true;
  
  try {
    const response = await getReaders(requestParams.value);
    readersData.value = response.results;
    pagination.value.total = response.count;
  } catch (error: any) {
    if (error.name !== 'AbortError') {
      console.error('Ошибка загрузки данных:', error);
      if (error.response?.status === 400) {
        dateError.value = 'Ошибка в параметрах запроса. Проверьте введенные данные.';
      } else {
        dateError.value = 'Произошла ошибка при загрузке данных. Попробуйте позже.';
      }
    }
  } finally {
    loading.value = false;
    abortController = null;
  }
};

const applyFilters = () => {
  if (!validateDates()) return;
  
  activeFilters.value = { ...localFilters.value };
  pagination.value.page = 1;
  loadReadersData();
};

watch(
  () => pagination.value.page,
  () => {
    loadReadersData();
  }
);

watch(
  [() => sortField.value, () => sortDirection.value],
  () => {
    pagination.value.page = 1;
    loadReadersData();
  }
);

const resetSorting = () => {
  sortField.value = 'id';
  sortDirection.value = 'asc';
};

const sortBy = (field: SortField) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortField.value = field;
    sortDirection.value = 'asc';
  }
};

const clearAllFilters = () => {
  localFilters.value = {
    fullname: '',
    department: '',
    registrationDateFrom: '',
    registrationDateTo: '',
    lastOrderDateFrom: '',
    lastOrderDateTo: '',
  };
  activeFilters.value = { ...localFilters.value };
  pagination.value.page = 1;
  resetSorting();
  loadReadersData();
};

const nextPage = () => {
  if (pagination.value.page < totalPages.value) {
    pagination.value.page++;
  }
};

const prevPage = () => {
  if (pagination.value.page > 1) {
    pagination.value.page--;
  }
};

onMounted(async () => {
  await loadReadersData();
});

onUnmounted(() => {
  if (abortController) {
    abortController.abort();
  }
});

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/");
  }
});
</script>

<style scoped lang="scss">
.readers-page {
  padding: 16px;
}

.page-header {
  margin-bottom: 1rem;
  
  h2 {
    color: var(--color-text-800);
    margin: 0;
  }
  
  .stats {
    color: var(--color-text-800);
    display: flex;
    align-items: center;
    gap: 1rem;
  }
}

.filters-section {
  background: var(--color-background-200);
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  border: 1px solid var(--color-text-200);
}

.filters-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  
  .filter-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--color-text-700);
    margin-bottom: 0.25rem;
  }
}

.filter-input {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-text-300);
  border-radius: 4px;
  background: white;
  font-size: 0.875rem;
  height: 2.25rem;
  
  &:focus {
    outline: none;
    border-color: var(--color-primary-500);
  }
  
  &:disabled {
    background: var(--color-background-300);
    cursor: not-allowed;
    opacity: 0.6;
  }
}

.date-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.date-separator {
  color: var(--color-text-500);
  font-size: 0.875rem;
  font-weight: 500;
  flex-shrink: 0;
}

.filter-actions {
  display: flex;
  gap: 0.5rem;
  align-items: end;
}

.apply-filters-btn {
  background: var(--color-primary-500);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  
  &:hover:not(:disabled) {
    background: var(--color-primary-600);
  }
  
  &:disabled {
    background: var(--color-text-300);
    cursor: not-allowed;
    opacity: 0.6;
  }
}

.clear-filters-btn {
  background: var(--color-primary-500);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  
  &:hover:not(:disabled) {
    background: var(--color-primary-600);
  }
  
  &:disabled {
    background: var(--color-text-300);
    cursor: not-allowed;
    opacity: 0.6;
  }
}

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
  position: relative;

  &:hover:not(.sort-loading) {
    background-color: var(--color-background-200);
  }

  &:focus {
    outline: 2px solid var(--color-primary-500);
    outline-offset: -2px;
  }

  &.active-sort {
    background-color: var(--color-background-300);
    
    .th-icon {
      opacity: 1;
      font-weight: bold;
    }
  }

  &.sort-loading {
    cursor: wait;
    opacity: 0.7;
    
    &::after {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(255, 255, 255, 0.5);
    }
  }

  &.sort-asc .direction-icon {
    color: var(--color-success-500);
  }

  &.sort-desc .direction-icon {
    color: var(--color-success-500);
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
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
  padding: 1rem;
}

.pagination-btn {
  background: var(--color-primary-500);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  
  &:hover:not(:disabled) {
    background: var(--color-primary-600);
  }
  
  &:disabled {
    background: var(--color-text-300);
    cursor: not-allowed;
    opacity: 0.6;
  }
}

.pagination-info {
  color: var(--color-text-600);
  font-size: 0.875rem;
}

.empty-state {
  padding: 3rem;
  text-align: center;
  color: var(--color-text-600);
}

.empty-state-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  border: 1px solid #fcc;
  font-size: 0.875rem;
}
</style>