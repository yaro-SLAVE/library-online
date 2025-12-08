<template>
  <div class="staff-page">
    <div class="page-header">
      <h2>Сотрудники</h2>
      <div class="stats">
        Всего сотрудников: {{ pagination.total }}
      </div>
    </div>

    <div class="search-section">
      <SearchInput
        v-model:modelValue="searchValue"
        @update:modelValue="handleSearch"
        :item-count="staffData.length"
      />
    </div>

    <StaffTable
      :staff-data="staffData"
      :loading="loading"
      :sort-field="sortField"
      :sort-direction="sortDirection"
      :pagination="pagination"
      :has-active-filters="hasSearch"
      @sort="handleSort"
      @prev-page="prevPage"
      @next-page="nextPage"
      @clear-filters="clearSearch"
      @row-click="showStaffOrders"
    />

    <StaffOrdersModal
      v-model:isOpen="isOrdersModalOpen"
      :staff="selectedStaff"
    />

    <LoadingModal v-model="loading" />
  </div>
</template>

<script setup lang="ts">
import StaffTable from '@moderator/components/StaffTable.vue';
import SearchInput from '@moderator/components/SearchInput.vue';
import LoadingModal from "@components/LoadingModal.vue";
import StaffOrdersModal from '@moderator/components/StaffOrdersModal.vue';

import { ref, onMounted, onUnmounted, computed } from "vue";
import { useAuthentication } from "@core/composables/auth";
import { useRouter } from "vue-router";
import { getStaffStats } from "@core/api/staff";
import type { StaffStats } from "@api/types";

const staffData = ref<StaffStats[]>([]);
const loading = ref(false);
const router = useRouter();
const searchValue = ref('');

const selectedStaff = ref<StaffStats>(null);
const isOrdersModalOpen = ref(false);

const pagination = ref({
  page: 1,
  limit: 10,
  total: 0
});

type SortField = 'fullname' | 'department' | 'total_orders' | 'cancelled_orders';

const sortField = ref<SortField>('fullname');
const sortDirection = ref<'asc' | 'desc'>('asc');

const hasSearch = computed(() => {
  return searchValue.value !== '';
});

let abortController: AbortController | null = null;

const requestParams = computed(() => {
  const params: any = {
    page: pagination.value.page,
    page_size: pagination.value.limit
  };
  
  if (searchValue.value) {
    params.search = searchValue.value;
  }
  
  if (sortField.value) {
    params.sort_by = sortField.value;
    params.sort_order = sortDirection.value;
  }
  
  return params;
});

const loadStaffData = async () => {
  if (abortController) {
    abortController.abort();
  }
  
  abortController = new AbortController();
  loading.value = true;
  
  try {
    const response = await getStaffStats(requestParams.value);
    staffData.value = response.results;
    pagination.value.total = response.count;
  } catch (error: any) {
    if (error.name !== 'AbortError') {
      console.error('Ошибка загрузки данных сотрудников:', error);
    }
  } finally {
    loading.value = false;
    abortController = null;
  }
};

const handleSearch = () => {
  pagination.value.page = 1;
  loadStaffData();
};

const handleSort = (field: string, direction: 'asc' | 'desc') => {
  sortField.value = field as SortField;
  sortDirection.value = direction;
  pagination.value.page = 1;
  loadStaffData();
};

const clearSearch = () => {
  searchValue.value = '';
  pagination.value.page = 1;
  loadStaffData();
};

const showStaffOrders = (staff: StaffStats) => {
  selectedStaff.value = staff;
  isOrdersModalOpen.value = true;
};

const nextPage = () => {
  if (pagination.value.page < totalPages.value) {
    pagination.value.page++;
    loadStaffData();
  }
};

const prevPage = () => {
  if (pagination.value.page > 1) {
    pagination.value.page--;
    loadStaffData();
  }
};

const totalPages = computed(() => 
  Math.ceil(pagination.value.total / pagination.value.limit)
);

onMounted(async () => {
  await loadStaffData();
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
.staff-page {
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

.search-section {
  margin-bottom: 1.5rem;
}
</style>