<template>
  <div v-if="modelValue" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Причина отмены</h2>
        <button class="close-button" @click="close">×</button>
      </div>

      <div class="modal-body">
        <div class="form-group">
          <select
            v-model="selectedReason"
            class="form-select"
            aria-label="Причина отмены заказа"
          >
            <option value="" disabled selected>Выберите причину отмены</option>
            <option
              v-for="reason in cancellationReasons"
              :key="reason.value"
              :value="reason.value"
            >
              {{ reason.label }}
            </option>
          </select>
        </div>

        <div class="comment-section">
          <h3>Свободный комментарий</h3>
          <textarea
            v-model="comment"
            placeholder="Введите дополнительный комментарий..."
            rows="3"
            class="comment-textarea"
          ></textarea>
        </div>
      </div>

      <div class="modal-footer">
        <StyledButton @click="confirm" theme="accent" :disabled="!selectedReason">
          Подтвердить отмену
        </StyledButton>
        <StyledButton @click="close" theme="secondary">Закрыть</StyledButton>
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
  (e: "confirm", reason: { reason: string; comment: string }): void;
}>();

// Причины отмены заказа
const cancellationReasons = ref([
  { value: "debt", label: "Не принес долги" },
  { value: "no_show", label: "В черном списке" },
  { value: "changed_mind", label: "Должник по учебе" },
]);

const selectedReason = ref("");
const comment = ref("");

const close = () => {
  emit("update:modelValue", false);
  // Сброс формы при закрытии
  selectedReason.value = "";
  comment.value = "";
};

const confirm = () => {
  if (selectedReason.value) {
    emit("confirm", {
      reason: selectedReason.value,
      comment: comment.value,
    });
    close();
  }
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
  width: min(100%, 40rem);
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

.form-group {
  margin-bottom: 1.5rem;
}

.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-text-200);
  border-radius: 0.5rem;
  font-size: 1rem;
  color: var(--color-text-700);
  background-color: var(--color-background-50);
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%234B5563'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1.25rem;
}

.form-select:focus {
  outline: none;
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
}

.comment-section {
  margin-top: 1.5rem;
}

.comment-section h3 {
  margin-bottom: 0.75rem;
  font-size: 1rem;
  color: var(--color-text-700);
  font-weight: 500;
}

.comment-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-text-200);
  border-radius: 0.5rem;
  resize: vertical;
  font-family: inherit;
  font-size: 0.875rem;
}

.comment-textarea:focus {
  outline: none;
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--color-text-100);
  display: flex;
  justify-content: space-between;
  background-color: var(--color-background-100);
}

@media (max-width: 640px) {
  .modal-content {
    width: 100%;
    margin: 1rem;
  }
  
  .modal-footer {
    flex-direction: column-reverse;
    gap: 0.75rem;
  }
  
  .modal-footer button {
    width: 100%;
  }
}
</style>