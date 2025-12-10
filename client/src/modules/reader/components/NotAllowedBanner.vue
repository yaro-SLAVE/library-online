<template>
  <ModalDialog v-model="open">
    <div class="dialog">
      <div title="Книги на руки выдаются только авторизованным читателям библиотеки">
        <InformationCircleIcon class="info" />
      </div>

      <h5><strong>Авторизуйтесь, чтобы сделать заказ</strong></h5>

      <div class="buttons">
        <StyledButton theme="primary" @click="goToProfile">Перейти к авторизации</StyledButton>
        <StyledButton theme="accent" @click="open = false">Закрыть</StyledButton>
      </div>
    </div>
  </ModalDialog>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { InformationCircleIcon } from "@heroicons/vue/24/outline";
import StyledButton from "@components/StyledButton.vue";
import ModalDialog from "@components/ModalDialog.vue";

const router = useRouter();
const open = defineModel<boolean>({ required: true });

// Переход на страницу профиля
const goToProfile = () => {
  open.value = false;
  router.push("/profile");
};
</script>

<style scoped lang="scss">
.dialog {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}

.info {
  width: 8rem;
  height: 8rem;
  &:hover {
    cursor: help;
  }
}

.buttons {
  display: flex;
  flex-direction: column;
  row-gap: 0.25rem;
}
</style>
