<template>
  <SurfaceCard class="surface">
    <form @submit.prevent="login">
      <div class="login-form">
        <h1 class="text-center">Вход</h1>
        <label for="username">Имя пользователя:</label>
        <TextField id="username" v-model="username" required class="field" />

        <label for="password">Пароль:</label>
        <PasswordTextField id="password" v-model="password" required class="field" />

        <StyledButton type="submit" class="auth-button">Войти</StyledButton>
        <a
          :href="`https://int.istu.edu/oauth/authorize?client_id=${OAUTH_CLIENT_ID}`"
          class="auth-button"
        >
          <StyledButton type="button" theme="secondary" class="w-full">
            Войти через кампус
          </StyledButton>
        </a>
        <a href="https://library.istu.edu/for-students/zapis-v-biblioteku/" class="auth-button">
          <StyledButton type="button" theme="secondary" class="w-full">
            Запись в библиотеку
          </StyledButton>
        </a>
      </div>
    </form>
  </SurfaceCard>

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
import PasswordTextField from "@components/PasswordTextField.vue";
import StyledButton from "@components/StyledButton.vue";
import SurfaceCard from "@components/SurfaceCard.vue";
import TextField from "@components/TextField.vue";
import ModalDialog from "@core/components/ModalDialog.vue";
import { useAuthStore } from "@core/store/auth";
import { ref } from "vue";
import { useUserStore } from "@core/store/user";
import { storeToRefs } from "pinia";
import type { Group } from "@core/api/types";

const OAUTH_CLIENT_ID = import.meta.env.VITE_OAUTH_CLIENT_ID;

const authStore = useAuthStore();

const userStore = useUserStore();

const openModal = ref(false);

const username = ref("");
const password = ref("");
async function login() {
  console.log(OAUTH_CLIENT_ID);
  // TODO: предупреждать пользователя об ошибках
  const r = await authStore.login(username.value, password.value);
  console.log(r);
  if(r) {
    await userStore.fetchProfile();
    const { currentUser } = storeToRefs(userStore);
    console.log(currentUser.value?.groups);
    if (currentUser.value?.groups?.includes("Librarian")) {
      openModal.value = true;
      console.log(currentUser.value?.groups, "YES");
    } else {
      console.log(currentUser.value?.groups, "NO");
      // router.push("/profile");
    }
  }
}

const handleUserRoleChoice = (choice: Group) => {
  userStore.setCurrentRole(choice);
  // router.push("/profile");
};
</script>

<style scoped lang="scss">
@use "@assets/styles/breakpoints.scss" as *;

.surface {
  margin-top: 20px;
}

.login-form {
  display: flex;
  flex-direction: column;

  margin: auto;
  min-width: 24rem;
}

.field {
  margin-bottom: 1rem;
}

label {
  font-weight: 600;
}

.auth-button {
  margin-bottom: 1rem;
  width: 100%;
}
</style>
