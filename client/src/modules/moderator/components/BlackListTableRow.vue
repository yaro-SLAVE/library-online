<template>
  <tr class="user-row">
    <td class="library-card">{{ user.library_card }}</td>
    <td class="fullname">{{ user.fullname }}</td>
    <td class="actions">
      <button 
        class="info-button"
        @click="handleUnban"
        :disabled="loading"
      >
        <span v-if="loading">Разблокировка...</span>
        <span v-else>Разблокировать</span>
      </button>
    </td>
  </tr>
</template>

<script setup lang="ts">
import type { BannedUser } from "@api/profile";

const props = defineProps<{
  user: BannedUser;
  loading: boolean;
}>();

const emit = defineEmits<{
  (e: "unbanUser", userId: number): void;
}>();

const handleUnban = () => {
  emit("unbanUser", props.user.id);
};
</script>

<style scoped lang="scss">
.user-row {
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
  word-break: break-all; /* Перенос длинных номеров */
  background-color: inherit;
  
  @media (max-width: 480px) {
    font-size: 0.85em;
  }
}

.fullname {
  color: var(--color-text-700);
  word-break: break-word; /* Перенос длинных ФИО */
  background-color: inherit;
  
  @media (max-width: 480px) {
    font-size: 0.9em;
  }
}

.actions {
  background-color: inherit;
}

.info-button {
  padding: 6px 10px;
  border: none;
  font-size: 0.9em;
  border-radius: 5px;
  cursor: pointer;
  background-color: var(--color-primary-400);
  color: var(--color-text-50);
  transition: background-color 0.2s;
  white-space: nowrap;

  &:hover:not(:disabled) {
    background-color: var(--color-primary-500);
  }

  &:disabled {
    background-color: var(--color-text-400);
    cursor: not-allowed;
    opacity: 0.7;
  }

  &:focus-visible {
    outline: 2px solid var(--color-primary-500);
    outline-offset: 2px;
  }
  
  @media (max-width: 480px) {
    padding: 5px 8px;
    font-size: 0.85em;
  }
}
</style>