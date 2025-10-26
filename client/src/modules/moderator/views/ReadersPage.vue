<template>
  <div class="readers-page">
    <div class="page-header">
      <h2>Читатели</h2>
      <div class="stats">
        Всего читателей: {{ readersData.length }}
        <button v-if="hasActiveFilters" @click="clearAllFilters" class="clear-filters-btn">
          Сбросить фильтры
        </button>
      </div>
    </div>

    <div class="filters-section">
      <div class="filter-row">
        <div class="filter-group">
          <label>ФИО читателя</label>
          <input 
            v-model="filters.fullname" 
            type="text" 
            placeholder="Поиск по ФИО..."
            class="filter-input"
            @input="onFilterChange"
          >
        </div>
        
        <div class="filter-group">
          <label>Количество книг от</label>
          <div class="range-inputs">
            <input 
              v-model.number="filters.minBooks" 
              type="number" 
              min="0"
              placeholder="Мин"
              class="filter-input"
              @change="onFilterChange"
            >
            <span class="filter-separator">до</span>
            <input 
              v-model.number="filters.maxBooks" 
              type="number" 
              min="0"
              placeholder="Макс"
              class="filter-input"
              @change="onFilterChange"
            >
          </div>
        </div>
        
        <div class="filter-group">
          <label>Количество заказов от</label>
          <div class="range-inputs">
            <input 
              v-model.number="filters.minOrders" 
              type="number" 
              min="0"
              placeholder="Мин"
              class="filter-input"
              @change="onFilterChange"
            >
            <span class="filter-separator">до</span>
            <input 
              v-model.number="filters.maxOrders" 
              type="number" 
              min="0"
              placeholder="Макс"
              class="filter-input"
              @change="onFilterChange"
            >
          </div>
        </div>
      </div>
      
      <div class="filter-row">
        <div class="filter-group">
          <label>Отмененные заказы от</label>
          <div class="range-inputs">
            <input 
              v-model.number="filters.minCancelled" 
              type="number" 
              min="0"
              placeholder="Мин"
              class="filter-input"
              @change="onFilterChange"
            >
            <span class="filter-separator">до</span>
            <input 
              v-model.number="filters.maxCancelled" 
              type="number" 
              min="0"
              placeholder="Макс"
              class="filter-input"
              @change="onFilterChange"
            >
          </div>
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
              :aria-sort="sortField === 'id' ? (sortDirection === 'asc' ? 'ascending' : 'descending') : 'none'"
            >
              <span class="th-content">
                #
                <div class="th-icon">
                  <span v-if="sortField === 'id'" class="direction-icon">
                    {{ sortDirection === 'asc' ? "↑" : "↓" }}
                  </span>
                  <span v-else>⇅</span>
                </div>
              </span>
            </th>
            <th
              @click="sortBy('fullname')"
              class="sortable-th"
              :aria-sort="sortField === 'fullname' ? (sortDirection === 'asc' ? 'ascending' : 'descending') : 'none'"
            >
              <span class="th-content">
                ФИО читателя
                <div class="th-icon">
                  <span v-if="sortField === 'fullname'" class="direction-icon">
                    {{ sortDirection === 'asc' ? "↑" : "↓" }}
                  </span>
                  <span v-else>⇅</span>
                </div>
              </span>
            </th>
            <th
              @click="sortBy('total_orders')"
              class="sortable-th"
              :aria-sort="sortField === 'total_orders' ? (sortDirection === 'asc' ? 'ascending' : 'descending') : 'none'"
            >
              <span class="th-content">
                Количество заказов
                <div class="th-icon">
                  <span v-if="sortField === 'total_orders'" class="direction-icon">
                    {{ sortDirection === 'asc' ? "↑" : "↓" }}
                  </span>
                  <span v-else>⇅</span>
                </div>
              </span>
            </th>
            <th
              @click="sortBy('total_books_ordered')"
              class="sortable-th"
              :aria-sort="sortField === 'total_books_ordered' ? (sortDirection === 'asc' ? 'ascending' : 'descending') : 'none'"
            >
              <span class="th-content">
                Количество заказанных книг
                <div class="th-icon">
                  <span v-if="sortField === 'total_books_ordered'" class="direction-icon">
                    {{ sortDirection === 'asc' ? "↑" : "↓" }}
                  </span>
                  <span v-else>⇅</span>
                </div>
              </span>
            </th>
            <th
              @click="sortBy('cancelled_orders')"
              class="sortable-th"
              :aria-sort="sortField === 'cancelled_orders' ? (sortDirection === 'asc' ? 'ascending' : 'descending') : 'none'"
            >
              <span class="th-content">
                Количество отмененных заказов
                <div class="th-icon">
                  <span v-if="sortField === 'cancelled_orders'" class="direction-icon">
                    {{ sortDirection === 'asc' ? "↑" : "↓" }}
                  </span>
                  <span v-else>⇅</span>
                </div>
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <ReadersTableRow v-for="reader in readersData" :key="reader.id" :reader="reader" />
        </tbody>
      </table>
      <div v-if="readersData.length === 0 && !loading" class="empty-state">
        <div v-if="hasActiveFilters" class="empty-state-content">
          <p>Нет читателей, соответствующих фильтрам</p>
          <button @click="clearAllFilters" class="clear-filters-btn">
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

import { type Order } from "@api/types";
import { type UserInfo } from "@api/types";

import { ref, onMounted, onUnmounted, computed } from "vue";
import { useAuthentication } from "@core/composables/auth";
import { useAuthStore } from "@core/store/auth";
import { useRouter } from "vue-router";

// TODO: вставить API запрос
// import

const readersData = ref<any[]>([]);
const loading = ref(false);
const authStore = useAuthStore();
const router = useRouter();

const filters = ref({
  fullname: '',
  minBooks: null as number | null,
  maxBooks: null as number | null,
  minOrders: null as number | null,
  maxOrders: null as number | null,
  minCancelled: null as number | null,
  maxCancelled: null as number | null,
  status: ''
});

const pagination = ref({
  page: 1,
  limit: 20,
  total: 0
});

type SortField = 'id' | 'fullname' | 'total_orders' | 'total_books_ordered' | 'cancelled_orders';

const sortField = ref<SortField>('id');
const sortDirection = ref<'asc' | 'desc'>('asc');

let filterTimeout: NodeJS.Timeout | null = null;

const hasActiveFilters = computed(() => {
  const f = filters.value;
  return f.fullname !== '' || 
         f.minBooks !== null || f.maxBooks !== null ||
         f.minOrders !== null || f.maxOrders !== null ||
         f.minCancelled !== null || f.maxCancelled !== null ||
         f.status !== '';
});

const loadReadersData = async () => {
  loading.value = true;
  try {
    const params: any = {};
    
    if (filters.value.fullname) params.fullname = filters.value.fullname;
    if (filters.value.minBooks !== null) params.min_books = filters.value.minBooks;
    if (filters.value.maxBooks !== null) params.max_books = filters.value.maxBooks;
    if (filters.value.minOrders !== null) params.min_orders = filters.value.minOrders;
    if (filters.value.maxOrders !== null) params.max_orders = filters.value.maxOrders;
    if (filters.value.minCancelled !== null) params.min_cancelled = filters.value.minCancelled;
    if (filters.value.maxCancelled !== null) params.max_cancelled = filters.value.maxCancelled;
    if (filters.value.status) params.status = filters.value.status;
    
    // сортировка
    if (sortField.value) {
      params.sort_by = sortField.value;
      params.sort_order = sortDirection.value;
    }
    
    // TODO: сделать вызов API
    // const response = await readers.getReaders(params);
    // readersData.value = response.data;
    
    console.log('Загрузка данных с фильтрами:', params);

    // TODO: убрать заглушку с имитацией API
    await new Promise(resolve => setTimeout(resolve, 500));
    readersData.value = getMockDataWithFilters(params);
    
  } catch (error) {
    console.error('Ошибка загрузки данных:', error);
  } finally {
    loading.value = false;
  }
};

const validateAllRanges = (): boolean => {
  const f = filters.value;
  const errors: string[] = [];
  
  if (f.minBooks !== null && f.maxBooks !== null && f.minBooks > f.maxBooks) {
    errors.push('Минимальное количество книг не может быть больше максимального');
  }
  
  if (f.minOrders !== null && f.maxOrders !== null && f.minOrders > f.maxOrders) {
    errors.push('Минимальное количество заказов не может быть больше максимального');
  }
  
  if (f.minCancelled !== null && f.maxCancelled !== null && f.minCancelled > f.maxCancelled) {
    errors.push('Минимальное количество отмененных заказов не может быть больше максимального');
  }
  
  if (errors.length > 0) {
    alert(errors.join('\n'));
    return false;
  }
  
  return true;
};

const onFilterChange = () => {
  if (!validateAllRanges()) {
    return;
  }
  
  if (filterTimeout) {
    clearTimeout(filterTimeout);
  }
  
  filterTimeout = setTimeout(() => {
    loadReadersData();
  }, 300);
};

const resetSorting = () => {
  sortField.value = 'id';
  sortDirection.value = 'asc';
  loadReadersData();
};

const sortBy = async (field: SortField) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortField.value = field;
    sortDirection.value = 'asc';
  }
  await loadReadersData();
};

const clearAllFilters = () => {
  filters.value = {
    fullname: '',
    minBooks: null,
    maxBooks: null,
    minOrders: null,
    maxOrders: null,
    minCancelled: null,
    maxCancelled: null,
    status: ''
  };
  sortField.value = 'id';
  loadReadersData();
};

// данные для теста
const getMockDataWithFilters = (params: any) => {
  const mockData = [
    {
      id: 1,
      user: {
        first_name: "Иван",
        last_name: "Петров",
        fullname: "Петров Иван Сергеевич",
        username: "i.petrov",
        department: "Институт информационных технологий и анализа данных",
        library_card: "12345"
      },
      total_books_ordered: 15,
      total_orders: 5,
      completed_orders: 3,
      cancelled_orders: 1
    },
    {
      id: 2,
      user: {
        first_name: "Мария",
        last_name: "Сидорова",
        fullname: "Сидорова Мария Ивановна",
        username: "m.sidorova",
        department: "Институт информационных технологий и анализа данных",
        library_card: "12346"
      },
      total_books_ordered: 8,
      total_orders: 3,
      completed_orders: 2,
      cancelled_orders: 0
    },
    {
      id: 3,
      user: {
        first_name: "Алексей",
        last_name: "Кузнецов",
        fullname: "Кузнецов Алексей Петрович",
        username: "a.kuznetsov",
        department: "Институт информационных технологий и анализа данных",
        library_card: "12347"
      },
      total_books_ordered: 22,
      total_orders: 7,
      completed_orders: 5,
      cancelled_orders: 2
    },
    {
      id: 4,
      user: {
        first_name: "Елена",
        last_name: "Васильева",
        fullname: "Васильева Елена Дмитриевна",
        username: "e.vasilyeva",
        department: "Институт информационных технологий и анализа данных",
        library_card: null
      },
      total_books_ordered: 3,
      total_orders: 2,
      completed_orders: 1,
      cancelled_orders: 1
    },
    {
      id: 5,
      user: {
        first_name: "Дмитрий",
        last_name: "Николаев",
        fullname: "Николаев Дмитрий Владимирович",
        username: "d.nikolaev",
        department: "Институт информационных технологий и анализа данных",
        library_card: "12348"
      },
      total_books_ordered: 12,
      total_orders: 4,
      completed_orders: 3,
      cancelled_orders: 0
    }
  ];

  // Имитация фильтрации на бэкенде
  return mockData.filter(reader => {
    if (params.fullname && !reader.user.fullname.toLowerCase().includes(params.fullname.toLowerCase())) {
      return false;
    }
    if (params.min_books !== null && reader.total_books_ordered < params.min_books) return false;
    if (params.max_books !== null && reader.total_books_ordered > params.max_books) return false;
    if (params.min_orders !== null && reader.total_orders < params.min_orders) return false;
    if (params.max_orders !== null && reader.total_orders > params.max_orders) return false;
    if (params.min_cancelled !== null && reader.cancelled_orders < params.min_cancelled) return false;
    if (params.max_cancelled !== null && reader.cancelled_orders > params.max_cancelled) return false;
    
    return true;
  });
};

onMounted(async () => {
  loadReadersData();
});

onUnmounted(() => {
  if (filterTimeout) {
    clearTimeout(filterTimeout);
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

.clear-filters-btn {
  background: var(--color-primary-500);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  
  &:hover {
    background: var(--color-primary-600);
  }
}

.filters-section {
  background: var(--color-background-200);
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  border: 1px solid var(--color-text-200);
}

.filter-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
  
  label {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--color-text-700);
  }
}

.range-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-input {
  padding: 0.5rem;
  border: 1px solid var(--color-text-300);
  border-radius: 4px;
  background: white;
  flex: 1;
  
  &:focus {
    outline: none;
    border-color: var(--color-primary-500);
  }
}

.filter-select {
  padding: 0.5rem;
  border: 1px solid var(--color-text-300);
  border-radius: 4px;
  background: white;
  
  &:focus {
    outline: none;
    border-color: var(--color-primary-500);
  }
}

.filter-separator {
  color: var(--color-text-600);
  font-size: 0.875rem;
  white-space: nowrap;
}

.column-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  font-size: 0.75rem;
  
  &:hover {
    background: var(--color-background-300);
  }
  
  &.active {
    background: var(--color-primary-200);
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

.empty-state {
  padding: 3rem;
  text-align: center;
  color: var(--color-text-600);
}
</style>