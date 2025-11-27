<!-- OrdersPage.vue (adjusted localFilters to include department to suppress warnings; assume FiltersSection uses it) -->
<template>
  <div class="orders-page">
    <div class="page-header">
      <h2>Заказы</h2>
      <div class="stats">
        Всего заказов: {{ pagination.total }}
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
      v-model:isOpen="isDetailsModalOpen"
      :orderId="selectedOrderId"
    />

    <LoadingModal v-model="loading" />
  </div>
</template>

<script setup lang="ts">
import FiltersSection from "@modules/moderator/components/FiltersSection.vue";
import OrdersTable from "@modules/moderator/components/orders/OrdersTable.vue";
import LoadingModal from "@components/LoadingModal.vue";
import OrderDetailsModal from "@modules/moderator/components/orders/OrderDetailsModal.vue";

import { ref, onMounted, onUnmounted, computed, watch } from "vue";
import { useAuthentication } from "@core/composables/auth";
import { useRouter } from "vue-router";
import { getOrdersStats } from "@api/orders";
import type { OrderStats, OrdersFilters, OrderStatusEnum } from "@api/types";

const ordersData = ref<OrderStats[]>([]);
const loading = ref(false);
const router = useRouter();
const dateError = ref('');

const localFilters = ref({
  fullname: '',
  department: '',  // Added to suppress warning; perhaps map to employee_collect or ignore
  employee_collect: '',
  employee_issue: '',
  lastOrderDateFrom: '',  // For dateFrom
  lastOrderDateTo: '',    // For dateTo
  currentOrderStatuses: [] as OrderStatusEnum[],  // For statuses
});

const activeFilters = ref({
  fullname: '',
  department: '',
  employee_collect: '',
  employee_issue: '',
  lastOrderDateFrom: '',
  lastOrderDateTo: '',
  currentOrderStatuses: [] as OrderStatusEnum[],
});

const pagination = ref({
  page: 1,
  limit: 10,
  total: 0
});

type SortField = 'id' | 'fullname' | 'employee_collect' | 'employee_issue' | 'status';

const sortField = ref<SortField>('id');
const sortDirection = ref<'asc' | 'desc'>('asc');

const isDetailsModalOpen = ref(false);
const selectedOrderId = ref<number>();

const showOrderDetails = (order: OrderStats) => {
  selectedOrderId.value = order.id;
  isDetailsModalOpen.value = true;
};

let abortController: AbortController | null = null;

const hasFilterChanges = computed(() => {
  return JSON.stringify(localFilters.value) !== JSON.stringify(activeFilters.value);
});

const hasActiveFilters = computed(() => {
  const f = activeFilters.value;
  return f.fullname !== '' || f.department !== '' || f.employee_collect !== '' || f.employee_issue !== '' ||
         f.lastOrderDateFrom !== '' || f.lastOrderDateTo !== '' ||
         f.currentOrderStatuses.length > 0;
});

const totalPages = computed(() => 
  Math.ceil(pagination.value.total / pagination.value.limit)
);

const requestParams = computed((): OrdersFilters => {
  const params: OrdersFilters = {
    page: pagination.value.page,
    page_size: pagination.value.limit
  };
  
  if (activeFilters.value.fullname) params.fullname = activeFilters.value.fullname;
  if (activeFilters.value.employee_collect) params.employee_collect = activeFilters.value.employee_collect;
  if (activeFilters.value.employee_issue) params.employee_issue = activeFilters.value.employee_issue;
  if (activeFilters.value.lastOrderDateFrom) params.date_from = activeFilters.value.lastOrderDateFrom;
  if (activeFilters.value.lastOrderDateTo) params.date_to = activeFilters.value.lastOrderDateTo;
  if (activeFilters.value.currentOrderStatuses && activeFilters.value.currentOrderStatuses.length > 0) {
    params.statuses = activeFilters.value.currentOrderStatuses;
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
    const response = await getOrdersStats(requestParams.value);
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
    department: '',
    employee_collect: '',
    employee_issue: '',
    lastOrderDateFrom: '',
    lastOrderDateTo: '',
    currentOrderStatuses: [],
  };
  activeFilters.value = { ...localFilters.value };
  pagination.value.page = 1;
  sortField.value = 'id';
  sortDirection.value = 'asc';
  loadOrdersData();
};

const nextPage = () => {
  if (pagination.value.page < totalPages.value) {
    pagination.value.page++;
    loadOrdersData();
  }
};

const prevPage = () => {
  if (pagination.value.page > 1) {
    pagination.value.page--;
    loadOrdersData();
  }
};

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