<template>
  <ModalDialog v-model="open">
    <div class="flex flex-col items-center">
      <h5>
        <strong class="title">{{ title }}</strong>
      </h5>
      <p class="content">{{ text }}</p>
      <div class="buttons">
        <StyledButton theme="accent" @click="confirmCancel">Да</StyledButton>
        <StyledButton theme="secondary" @click="open = false">Нет</StyledButton>
      </div>
    </div>
  </ModalDialog>
</template>

<script setup lang="ts">
import StyledButton from "./StyledButton.vue";
import ModalDialog from "./ModalDialog.vue";
const { title, text } = defineProps<{
  title: string;
  text: string;
}>();

const emit = defineEmits<{
  (e: "confirm"): void;
}>();

const open = defineModel<boolean>({ required: true });

const confirmCancel = () => {
  emit("confirm");
  open.value = false;
};
</script>

<style scoped lang="scss">
.title {
  color: var(--color-text-800);
}

.content {
  color: var(--color-text-700);
}

.buttons {
  margin-top: 1rem;
  display: flex;
  flex-direction: row;
  column-gap: 1rem;
}
</style>
