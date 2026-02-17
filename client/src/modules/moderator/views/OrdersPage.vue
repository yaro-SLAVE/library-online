<template>
  <div class="orders-page">
    <div class="page-header">
      <h2>Заказы</h2>
      <div class="stats">
        Всего заказов: {{ pagination.total }}
      </div>
    </div>

    <OrdersFiltersSection
      v-model:filters="localFilters"
      :loading="loading"
      :date-error="dateError"
      :has-active-filters="hasActiveFilters"
      :has-filter-changes="hasFilterChanges"
      @apply-filters="applyFilters"
      @clear-filters="clearAllFilters"
    />

    <OrdersTable
      :orders-data="ordersData"
      :loading="loading"
      :sort-field="sortField"
      :sort-direction="sortDirection"
      :pagination="pagination"
      :has-active-filters="hasActiveFilters"
      @sort="handleSort"
      @prev-page="prevPage"
      @next-page="nextPage"
      @clear-filters="clearAllFilters"
      @row-click="showOrderDetails"
    />

    <OrderDetailsModal
      v-if="selectedOrder"
      v-model:isOpen="isDetailsModalOpen"
      :order-id="selectedOrder.id"
    />

    <LoadingModal :model-value="loading" />
  </div>
</template>

<script setup lang="ts">
import OrdersFiltersSection from "@moderator/components/orders/OrdersFiltersSection.vue";
import OrdersTable from "@moderator/components/orders/OrdersTable.vue";
import LoadingModal from "@components/LoadingModal.vue";
import OrderDetailsModal from "@moderator/components/orders/OrderDetailsModal.vue";

import { ref, onMounted, onUnmounted, computed, watch } from "vue";
import { useAuthentication } from "@core/composables/auth";
import { useRouter } from "vue-router";
import { getModeratorOrders } from "@api/orders";
import type { ModeratorOrderStats, ModeratorOrdersFilters, OrderStatusEnum } from "@api/types";

const ordersData = ref<ModeratorOrderStats[]>([]);
const loading = ref(false);
const router = useRouter();
const dateError = ref('');

const localFilters = ref({
  fullname: '',
  libraryName: '',
  employeeCollect: '',
  employeeIssue: '',
  dateFrom: '',
  dateTo: '',
  statuses: [] as OrderStatusEnum[],
});

const activeFilters = ref({
  fullname: '',
  libraryName: '',
  employeeCollect: '',
  employeeIssue: '',
  dateFrom: '',
  dateTo: '',
  statuses: [] as OrderStatusEnum[],
});

const pagination = ref({
  page: 1,
  limit: 10,
  total: 0
});

type SortField = 'id' | 'fullname' | 'library' | 'employee_collect' | 'employee_issue' | 'status' | 'created_date' | 'books_count';

const sortField = ref<SortField>('created_date');
const sortDirection = ref<'asc' | 'desc'>('desc');

const isDetailsModalOpen = ref(false);
const selectedOrder = ref<ModeratorOrderStats | null>(null);

const showOrderDetails = (order: ModeratorOrderStats) => {
  selectedOrder.value = order;
  isDetailsModalOpen.value = true;
};

let abortController: AbortController | null = null;

const hasFilterChanges = computed(() => {
  return JSON.stringify(localFilters.value) !== JSON.stringify(activeFilters.value);
});

const hasActiveFilters = computed(() => {
  const f = activeFilters.value;
  return f.fullname !== '' || f.libraryName !== '' || 
         f.employeeCollect !== '' || f.employeeIssue !== '' ||
         f.dateFrom !== '' || f.dateTo !== '' ||
         f.statuses.length > 0;
});

const totalPages = computed(() => 
  Math.ceil(pagination.value.total / pagination.value.limit)
);

const requestParams = computed((): ModeratorOrdersFilters => {
  const params: ModeratorOrdersFilters = {
    page: pagination.value.page,
    page_size: pagination.value.limit
  };
  
  if (activeFilters.value.fullname) params.fullname = activeFilters.value.fullname;
  if (activeFilters.value.libraryName) params.library_name = activeFilters.value.libraryName;
  if (activeFilters.value.employeeCollect) params.employee_collect = activeFilters.value.employeeCollect;
  if (activeFilters.value.employeeIssue) params.employee_issue = activeFilters.value.employeeIssue;
  if (activeFilters.value.dateFrom) params.date_from = activeFilters.value.dateFrom;
  if (activeFilters.value.dateTo) params.date_to = activeFilters.value.dateTo;
  if (activeFilters.value.statuses && activeFilters.value.statuses.length > 0) {
    params.statuses = activeFilters.value.statuses;
  }
  
  if (sortField.value) {
    params.sort_by = sortField.value;
    params.sort_order = sortDirection.value;
  }
  
  return params;
});

const validateDates = (): boolean => {
  dateError.value = '';
  
  if (!validateDateRange(localFilters.value.dateFrom, localFilters.value.dateTo)) {
    dateError.value = 'Дата начала не может быть больше даты окончания';
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

const loadOrdersData = async () => {
  if (!validateDates()) return;
  
  if (abortController) {
    abortController.abort();
  }
  
  abortController = new AbortController();
  loading.value = true;
  
  try {
    const response = await getModeratorOrders(requestParams.value);
    ordersData.value = response.results;
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
  loadOrdersData();
};

const handleSort = (field: string, direction: 'asc' | 'desc') => {
  sortField.value = field as SortField;
  sortDirection.value = direction;
  pagination.value.page = 1;
  loadOrdersData();
};

const clearAllFilters = () => {
  localFilters.value = {
    fullname: '',
    libraryName: '',
    employeeCollect: '',
    employeeIssue: '',
    dateFrom: '',
    dateTo: '',
    statuses: [],
  };
  activeFilters.value = { ...localFilters.value };
  pagination.value.page = 1;
  sortField.value = 'created_date';
  sortDirection.value = 'desc';
  loadOrdersData();
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
    loadOrdersData();
  }
);

onMounted(async () => {
  await loadOrdersData();
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
.orders-page {
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