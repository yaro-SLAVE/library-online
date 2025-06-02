<template>
  <div v-if="modelValue" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Укажите причину отката заказа</h2>
        <button class="close-button" @click="close">×</button>
      </div>

      <div class="modal-body">
        <div class="comment-card">
          <textarea v-model="rejectReason" placeholder="Введите причину отката..." rows="4">
          </textarea>
        </div>
      </div>

      <div class="modal-footer">
        <StyledButton @click="close" theme="secondary">Отмена</StyledButton>
        <StyledButton @click="confirm" theme="accent">Подтвердить</StyledButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import StyledButton from "@components/StyledButton.vue";

defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
  (e: "confirm", reason: string): void;
}>();

const rejectReason = ref("");

const close = () => {
  emit("update:modelValue", false);
};

const confirm = () => {
  emit("confirm", rejectReason.value);
  close();
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: grid;
  place-items: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: var(--color-background-50);
  border-radius: 0.5rem;
  width: min(100%, 56rem);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.2);
  border: 1px solid var(--color-text-200);
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--color-text-100);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--color-background-100);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.375rem;
  color: var(--color-text-800);
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text-400);
  padding: 0 0.5rem;
  line-height: 1;
  transition: color 0.2s;
}

.close-button:hover {
  color: var(--color-primary-600);
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex-grow: 1;
}

.comment-card {
  display: flex;
  flex-direction: column;
}
.comment-card textarea {
  width: 100%;
  min-height: 50px;
  padding: 0.75rem;
  border: 1px solid var(--color-text-200);
  border-radius: 0.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--color-text-100);
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  background-color: var(--color-background-100);
}
</style>
