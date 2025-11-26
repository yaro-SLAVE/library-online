<template>
  <tr class="candidate-row">
    <td class="library-card">{{ candidate.library_card }}</td>
    <td class="fullname">{{ candidate.fullname }}</td>
    <td class="total-orders">{{ candidate.total_orders_count }}</td>
    <td class="cancelled-orders">{{ candidate.cancelled_orders_count }}</td>
    <td class="actions">
      <button 
        class="ban-button"
        @click="handleBan"
        :disabled="loading"
      >
        <span v-if="loading">Блокировка...</span>
        <span v-else>Заблокировать</span>
      </button>
    </td>
  </tr>
</template>

<script setup lang="ts">
import type { BanCandidate } from "@api/profile";

const props = defineProps<{
  candidate: BanCandidate;
  loading: boolean;
}>();

const emit = defineEmits<{
  (e: "banUser", userId: number): void;
}>();

const handleBan = () => {
  emit("banUser", props.candidate.user_id);
};
</script>

<style scoped lang="scss">
.candidate-row {
  transition: background-color 0.2s;
  background-color: var(--color-background-100);

  &:hover {
    background-color: var(--color-background-200);
  }
}

.library-card {
  font-weight: 500;
  font-family: monospace;
  color: var(--color-text-800);
  font-size: 0.9em;
  word-break: break-all;
  background-color: inherit;
  
  @media (max-width: 480px) {
    font-size: 0.85em;
  }
}

.fullname {
  color: var(--color-text-700);
  word-break: break-word;
  background-color: inherit;
  
  @media (max-width: 480px) {
    font-size: 0.9em;
  }
}

.total-orders,
.cancelled-orders {
  text-align: center;
  font-weight: 500;
  background-color: inherit;
}

.cancelled-orders {
  color: var(--color-accent-400);
}

.actions {
  background-color: inherit;
}

.ban-button {
  padding: 6px 10px;
  border: none;
  font-size: 0.9em;
  border-radius: 5px;
  cursor: pointer;
  background-color: var(--color-accent-400);
  color: var(--color-text-50);
  transition: background-color 0.2s;
  white-space: nowrap;

  &:hover:not(:disabled) {
    background-color: var(--color-accent-500);
  }

  &:disabled {
    background-color: var(--color-text-400);
    cursor: not-allowed;
    opacity: 0.7;
  }

  &:focus-visible {
    outline: 2px solid var(--color-accent-500);
    outline-offset: 2px;
  }
  
  @media (max-width: 480px) {
    padding: 5px 8px;
    font-size: 0.85em;
  }
}
</style>