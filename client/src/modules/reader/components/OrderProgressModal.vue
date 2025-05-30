<template>
  <ModalDialog v-model="open" :esc-close="false" :mask-closable="false">
    <motion.div
      class="order-modal"
      :initial="{ opacity: 0, y: -10 }"
      :animate="{ opacity: 1, y: 0 }"
      :transition="{ duration: 0.7, ease: 'easeOut' }"
    >
      <motion.div
        class="modal-header"
        :initial="{ opacity: 0, y: -10 }"
        :animate="{ opacity: 1, y: 0 }"
        :transition="{ duration: 0.7, ease: 'easeOut' }"
      >
        <h3>Оформление заказа</h3>
      </motion.div>
      <ul class="steps-list">
        <li
          v-for="(step, index) in state.steps"
          :key="index"
          class="step-item"
          :class="{ error: state.isError }"
        >
          <div class="step-icon-container">
            <motion.div
              v-if="animationStep === index && !state.isError && animationStep < 5"
              class="spinner"
              :animate="{
                rotate: [0, 360],
              }"
              :transition="{
                repeat: Infinity,
                duration: 1,
                ease: 'linear',
              }"
            >
            </motion.div>

            <motion.div
              v-if="animationStep > index || (isLastStep && state.isSuccess)"
              class="checkmark"
              :initial="{ scale: 0, opacity: 0 }"
              :animate="{ scale: 1, opacity: 1 }"
              :transition="{ type: 'spring', stiffness: 500, damping: 20 }"
            >
              ✓
            </motion.div>
          </div>

          <motion.div
            class="step-content"
            :initial="{ x: -10, opacity: 0 }"
            :animate="{ x: 0, opacity: 1 }"
            :transition="{ duration: 0.3, ease: 'easeOut' }"
          >
            <h3
              :class="{
                active: animationStep > index || (isLastStep && state.isSuccess),
                'error-text': step.error && index == state.currentStep,
              }"
            >
              {{ step.title }}
            </h3>
            <template v-if="step.messages !== null">
              <div v-for="msg in step.messages" :key="msg" class="messages">
                <div class="message-item">
                  {{ msg }}
                </div>
              </div>
            </template>
            <p v-if="state.currentStep === index && state.isError" class="step-error">
              {{ step.error }}
            </p>
          </motion.div>
        </li>
      </ul>

      <motion.div
        v-if="state.isSuccess && isLastStep"
        class="result-message success"
        :initial="{ opacity: 0, scale: 0.9 }"
        :animate="{ opacity: 1, scale: 1 }"
        :transition="{ duration: 0.4, ease: 'easeOut' }"
      >
        <h4>Заказ успешно оформлен!</h4>
      </motion.div>

      <motion.div
        v-if="state.isError && isLastStep"
        class="result-message error"
        :initial="{ opacity: 0, y: 20 }"
        :animate="{ opacity: 1, y: 0 }"
        :transition="{ duration: 0.4, ease: 'easeOut' }"
      >
        <h4>Ошибка оформления заказа</h4>
      </motion.div>
    </motion.div>
    <div class="btn-close-modal">
        <StyledButton v-if="state.isError || state.currentStep === 5" @click="handleCLoseClick">
          Закрыть окно
        </StyledButton>
      </div>
  </ModalDialog>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { motion } from "motion-v";
import ModalDialog from "@components/ModalDialog.vue";
import StyledButton from "@components/StyledButton.vue";
import router from "@core/router/index";

type ModalStep = {
  title: string;
  error: string;
  messages: string[] | null;
};

type ModalState = {
  isOpen: boolean;
  currentStep: number;
  steps: ModalStep[];
  isSuccess: boolean;
  isError: boolean;
};

const open = defineModel<boolean>({ required: true });
const animationStep = ref(0);
const isLastStep = computed(() => {
  return animationStep.value == 5;
});
const props = defineProps({
  state: {
    type: Object as () => ModalState,
    required: true,
  },
});

setInterval(async () => {
  if ((await props.state.currentStep) > animationStep.value) {
    animationStep.value++;
  }
}, 800);

const handleCLoseClick = () => {
  open.value = false;
  if (props.state.isSuccess) {
    router.push("/");
  }
};
</script>

<style lang="scss" scoped>
.btn-close-modal {
  display: flex;
  justify-content: center;
}

.order-modal {
  max-width: 500px;
  margin: 5vh auto;
  padding: 2rem;
  border-radius: 20px;
  background: var(--color-surface-100);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.modal-header {
  margin-bottom: 2rem;
  text-align: center;

  h3 {
    font-size: 2.5rem;
    color: var(--color-text-900);
  }
}

.steps-list {
  .step-item {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
    align-items: center;
  }

  .step-icon-container {
    position: relative;
    min-width: 32px;
    min-height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .step-content {
    flex-grow: 1;

    h3 {
      margin: 0 0 4px 0;
      font-size: 1.5rem;
      color: var(--color-text-600);
      font-weight: 300;
      transition:
        color 0.3s,
        font-weight 0.3s;

      &.active {
        color: var(--color-text-900);
        font-weight: 600;
      }

      &.error-text {
        color: var(--color-status-error);
      }
    }
  }
}

.spinner {
  position: absolute;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 3px solid var(--color-status-new);
  border-top-color: transparent;
  background: none;
  display: flex;
  align-items: center;
  justify-content: center;
}
.checkmark {
  position: absolute;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-status-done);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.step-error {
  background: rgba(244, 67, 54, 0.1);
  border-radius: 30px;
  padding: 1rem;
  color: var(--color-status-error);
  font-size: 0.9em;
}

.result-message {
  text-align: center;
  padding: 0.1rem 1rem;
  border-radius: 8px;
  h4 {
    font-size: 26px;
  }
  &.success {
    color: var(--color-text-600);
  }

  &.error {
    color: var(--color-text-600);
  }
}

.messages {
  .message-item {
    display: flex;
    padding: 1rem;
    font-weight: 300;
    border-radius: 30px;
    color: var(--color-status-done);
  }
}
</style>
