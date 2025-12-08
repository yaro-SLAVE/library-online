<template>
  <tr class="reader-row" @click="handleRowClick">
    <td>{{ order.id }}</td>
    <td>{{ order.fullname }}</td>
    <td>{{ order.employee_collect || '-' }}</td>
    <td>{{ order.employee_issue || '-' }}</td>
    <td>{{ lastStatusLabel }}</td>
  </tr>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { OrderStats } from "@api/types";
import { orderStatuses } from "@api/types";
import type { OrderStatusEnum } from "@api/types";

interface Props {
  order: OrderStats;
  lastStatus?: string;
}

interface Emits {
  (e: 'row-click', order: OrderStats): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const handleRowClick = () => emit('row-click', props.order);

const mapStatusKeyToLabel = (key: unknown): string | undefined => {
  if (typeof key !== 'string') return undefined;
  // безопасная проверка наличия ключа в объекте
  if (key in orderStatuses) {
    return orderStatuses[key as OrderStatusEnum];
  }
  return undefined;
};

const lastStatusLabel = computed(() => {
  // если таблица заранее передала готовую метку — используем её
  if (props.lastStatus) return props.lastStatus;

  const o: any = props.order;

  if (Array.isArray(o.statuses) && o.statuses.length > 0) {
    const last = o.statuses[o.statuses.length - 1];
    // сначала пробуем маппинг ключ -> метка
    const labelFromMap = mapStatusKeyToLabel(last?.status);
    return labelFromMap ?? last?.status ?? '-';
  }

  // если нет истории, пробуем сопоставить order.status, иначе fallback
  const labelFromMap = mapStatusKeyToLabel(o.status);
  return labelFromMap ?? o.status ?? '-';
});
</script>

<style scoped lang="scss">
.reader-row {
  cursor: pointer;
  transition: background-color 0.2s;
  background-color: var(--color-background-100);

  &:hover {
    background-color: var(--color-background-200);
  }

  td {
    padding: 12px;
    text-align: left;
    color: var(--color-text-800);
    border-bottom: 1px solid var(--color-text-200);
    background-color: transparent;
  }
}
</style>
