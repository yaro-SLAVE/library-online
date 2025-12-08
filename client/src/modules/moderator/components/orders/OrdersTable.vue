<template>
  <div class="table-container">
    <table class="table">
      <thead>
        <tr>
          <SortableHeader
            field="id"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            #
          </SortableHeader>

          <SortableHeader
            field="fullname"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            ФИО читателя
          </SortableHeader>

          <SortableHeader
            field="employee_collect"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Сотрудник собрал
          </SortableHeader>

          <SortableHeader
            field="employee_issue"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Сотрудник выдал
          </SortableHeader>

          <SortableHeader
            field="status"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Статус
          </SortableHeader>
        </tr>
      </thead>
      <tbody>
        <OrdersTableRow 
          v-for="order in normalizedOrders" 
          :key="order.id" 
          :order="order" 
          :last-status="order._lastStatusLabel"
          @row-click="$emit('row-click', $event)"
        />
      </tbody>
    </table>

    <Pagination
      v-if="normalizedOrders.length > 0"
      :current-page="pagination.page"
      :total-pages="totalPages"
      :loading="loading"
      @prev="prevPage"
      @next="nextPage"
    />

    <EmptyState
      v-if="normalizedOrders.length === 0 && !loading"
      :has-active-filters="hasActiveFilters"
      @clear-filters="$emit('clear-filters')"
      :loading="loading"
    />
  </div>
</template>

<script setup lang="ts">
import OrdersTableRow from "../orders/OrdersTableRow.vue";
import SortableHeader from '@modules/moderator/components/SortableHeader.vue';
import Pagination from '@modules/moderator/components/Pagination.vue';
import EmptyState from '@modules/moderator/components/EmptyState.vue';
import type { OrderStats } from "@api/types";
import { computed } from 'vue';
import { orderStatuses } from "@api/types";
import type { OrderStatusEnum } from "@api/types";

interface Props {
  ordersData: OrderStats[];
  loading: boolean;
  sortField: string;
  sortDirection: 'asc' | 'desc';
  pagination: {
    page: number;
    total: number;
    limit: number;
  };
  hasActiveFilters: boolean;
}

interface Emits {
  (e: 'sort', field: string, direction: 'asc' | 'desc'): void;
  (e: 'prev-page'): void;
  (e: 'next-page'): void;
  (e: 'clear-filters'): void;
  (e: 'row-click', order: OrderStats): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const totalPages = computed(() => 
  Math.ceil(props.pagination.total / props.pagination.limit)
);

const onSort = (field: string, direction: 'asc' | 'desc') => {
  emit('sort', field, direction);
};

const prevPage = () => {
  emit('prev-page');
};

const nextPage = () => {
  emit('next-page');
};

// нормализуем список заказов и заранее считаем метку последнего статуса
const normalizedOrders = computed(() => {
  return props.ordersData.map((o: any) => {
    let label = '-';

    if (Array.isArray(o.statuses) && o.statuses.length > 0) {
      const last = o.statuses[o.statuses.length - 1];
      if (typeof last?.status === 'string' && last.status in orderStatuses) {
        label = orderStatuses[last.status as OrderStatusEnum];
      } else {
        label = last?.status ?? '-';
      }
    } else {
      if (typeof o.status === 'string' && o.status in orderStatuses) {
        label = orderStatuses[o.status as OrderStatusEnum];
      } else {
        label = o.status ?? '-';
      }
    }

    return { ...o, _lastStatusLabel: label };
  });
});

</script>

<style scoped lang="scss">
.table-container {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

th {
  padding: 12px;
  text-align: left;
  color: var(--color-text-800);
  background-color: var(--color-background-100);
}

tr {
  border-bottom: 1px solid var(--color-text-200);
}
</style>
