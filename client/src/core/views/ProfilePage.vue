<template>
  <div class="container">
    <LoginForm v-if="!isAuthenticated" />
    <div v-else class="profile">
      <h3 class="text-center">{{ currentUser?.first_name }} {{ currentUser?.last_name }}</h3>
      <h4 class="text-center">{{ currentUser?.username }}</h4>
      <h5 class="text-center">
        {{ groups[currentRole] }}
      </h5>
      <StyledButton theme="accent" class="w-full" @click="handleLogout">Выйти</StyledButton>
    </div>
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
import { groups } from "@api/types";
import StyledButton from "@components/StyledButton.vue";
import LoginForm from "@modules/reader/components/LoginForm.vue";
import ModalDialog from "@core/components/ModalDialog.vue";
import { useAuthStore } from "@core/store/auth";
import { useUserStore } from "@core/store/user";
import { storeToRefs } from "pinia";
import router from "@core/router/index";
import type { Group } from "@core/api/types";
import { ref, onBeforeMount } from "vue";

const authStore = useAuthStore();
const userStore = useUserStore();
const { isAuthenticated } = storeToRefs(authStore);
const { currentUser, currentRole } = storeToRefs(userStore);

const handleLogout = () => {
  router.push("/");
  authStore.logout();
};

const openModal = ref(false);

onBeforeMount(() => {
  if (isAuthenticated) {
  if (currentUser.value?.groups?.includes("Librarian")) {
      openModal.value = true;
      console.log(currentUser.value?.groups, "YES");
    } else {
      console.log(currentUser.value?.groups, "NO");
      // router.push("/profile");
    }
  }
});

const handleUserRoleChoice = (choice: Group) => {
  userStore.setCurrentRole(choice);
  openModal.value = false;
  router.push("/");
};


</script>

<style scoped lang="scss">
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile {
  width: 50%;
  margin: auto;
}
</style>
