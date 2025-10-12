<template>
  <div class="text-center">
    <h1>
      {{ states[state] }}
    </h1>
  </div>
  <ModalDialog v-model="openModal">
    <h4 class="modal-text">Зайти как сотрудник<br />или как читатель ?</h4>
    <div class="choice-buttons">
      <StyledButton @click="handleUserRoleChoice('Reader')"> Читатель </StyledButton>
      <StyledButton @click="handleUserRoleChoice('Librarian')" theme="accent">
        Сотрудник
      </StyledButton>
    </div>
  </ModalDialog>
</template>

<script setup lang="ts">
import { useAuthStore } from "@core/store/auth";
import { onBeforeMount, ref } from "vue";
import { useRouter } from "vue-router";

import { storeToRefs } from "pinia";
import StyledButton from "@core/components/StyledButton.vue";
import ModalDialog from "@core/components/ModalDialog.vue";
import type { Group } from "@core/api/types";
const openModal = ref(false);
const router = useRouter();
const authStore = useAuthStore();
const states = {
  loading: "Загрузка...",
  error: "Ошибка",
  auth: "Авторизация...",
  success: "Успешно",
};

const state = ref<keyof typeof states>("loading");

onBeforeMount(async () => {
  const code = router.currentRoute.value.query["code"];
  if (typeof code === "string") {
    state.value = "auth";
    const success = await authStore.bitrixLogin(code);
    if (success) {
      const { currentUser } = storeToRefs(authStore);
      if (currentUser.value?.groups?.includes("Librarian")) {
        openModal.value = true;
        console.log(currentUser.value?.groups, "YES");
      } else {
        console.log(currentUser.value?.groups, "NO");
        state.value = "success";
        router.push("/profile");
      }
      state.value = "success";
    } else {
      state.value = "error";
    }
  } else {
    state.value = "error";
  }
});

const handleUserRoleChoice = (choice: Group) => {
  authStore.setUserRole(choice);
  state.value = "success";
  router.push("/profile");
};
</script>

<style lang="scss" scoped>
.modal-text {
  color: var(--color-text-500);
}
.choice-buttons {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 3rem;
}
</style>
