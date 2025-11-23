<template>
  <div class="readers-page">
    <div class="page-header">
      <h2>Читатели</h2>
      <div class="stats">
        Всего читателей: {{ pagination.total }}
      </div>
    </div>

    <FiltersSection
      v-model:filters="localFilters"
      :loading="loading"
      :date-error="dateError"
      :has-active-filters="hasActiveFilters"
      :has-filter-changes="hasFilterChanges"
      @apply-filters="applyFilters"
      @clear-filters="clearAllFilters"
    />

    <ReadersTable
      :readers-data="readersData"
      :loading="loading"
      :sort-field="sortField"
      :sort-direction="sortDirection"
      :pagination="pagination"
      :has-active-filters="hasActiveFilters"
      @sort="handleSort"
      @prev-page="prevPage"
      @next-page="nextPage"
      @clear-filters="clearAllFilters"
      @row-click="showReaderOrders"
    />

    <ReaderOrdersModal
      v-model:isOpen="isOrdersModalOpen"
      :reader="selectedReader"
    />

    <LoadingModal v-model="loading" />
  </div>
</template>

<script setup lang="ts">
import FiltersSection from "@modules/moderator/components/FiltersSection.vue";
import ReadersTable from "@modules/moderator/components/ReadersTable.vue";
import LoadingModal from "@components/LoadingModal.vue";
import ReaderOrdersModal from "@modules/moderator/components/ReaderOrdersModal.vue";

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
  lastOrderDateFrom: '',
  lastOrderDateTo: '',
  currentOrderStatuses: [],
});

const activeFilters = ref({
  fullname: '',
  department: '',
  lastOrderDateFrom: '',
  lastOrderDateTo: '',
  currentOrderStatuses: [],
});

const pagination = ref({
  page: 1,
  limit: 10,
  total: 0
});

type SortField = 'id' | 'fullname' | 'department' | 'total_books_ordered' | 'total_orders' | 'cancelled_orders';

const sortField = ref<SortField>('id');
const sortDirection = ref<'asc' | 'desc'>('asc');

const isOrdersModalOpen = ref(false);
const selectedReader = ref<ReaderStats>();

const showReaderOrders = (reader: ReaderStats) => {
  selectedReader.value = reader;
  isOrdersModalOpen.value = true;
};

let abortController: AbortController | null = null;

const hasFilterChanges = computed(() => {
  return JSON.stringify(localFilters.value) !== JSON.stringify(activeFilters.value);
});

const hasActiveFilters = computed(() => {
  const f = activeFilters.value;
  return f.fullname !== '' || f.department !== '' || 
         f.lastOrderDateFrom !== '' || f.lastOrderDateTo !== '' ||
         f.currentOrderStatuses.length > 0;
});

const totalPages = computed(() => 
  Math.ceil(pagination.value.total / pagination.value.limit)
);

const requestParams = computed((): ReadersFilters => {
  const params: ReadersFilters = {
    page: pagination.value.page,
    page_size: pagination.value.limit
  };
  
  if (activeFilters.value.fullname) params.fullname = activeFilters.value.fullname;
  if (activeFilters.value.department) params.department = activeFilters.value.department;
  if (activeFilters.value.lastOrderDateFrom) params.last_order_date_from = activeFilters.value.lastOrderDateFrom;
  if (activeFilters.value.lastOrderDateTo) params.last_order_date_to = activeFilters.value.lastOrderDateTo;
  if (activeFilters.value.currentOrderStatuses && activeFilters.value.currentOrderStatuses.length > 0) {
    params.current_order_statuses = activeFilters.value.currentOrderStatuses;
  }
  
  if (sortField.value) {
    params.sort_by = sortField.value;
    params.sort_order = sortDirection.value;
  }
  
  return params;
});

const validateDates = (): boolean => {
  dateError.value = '';
  
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

const handleSort = (field: string, direction: 'asc' | 'desc') => {
  sortField.value = field as SortField;
  sortDirection.value = direction;
};

const clearAllFilters = () => {
  localFilters.value = {
    fullname: '',
    department: '',
    lastOrderDateFrom: '',
    lastOrderDateTo: '',
    currentOrderStatuses: [],
  };
  activeFilters.value = { ...localFilters.value };
  pagination.value.page = 1;
  sortField.value = 'id';
  sortDirection.value = 'asc';
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
</style>