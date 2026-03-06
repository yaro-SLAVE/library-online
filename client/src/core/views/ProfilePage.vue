<template>
  <div class="container">
    <LoginForm v-if="!isAuthenticated" />
    <div v-else class="profile">
      <h3 class="text-center">{{ currentUser?.first_name }} {{ currentUser?.last_name }}</h3>
      <h4 class="text-center">{{ currentUser?.username }}</h4>
      <h5 class="text-center">
        {{ currentRole }}
      </h5>
      <StyledButton theme="accent" class="w-full" @click="handleLogout">Выйти</StyledButton>
    </div>
  </div>

  
  <ModalDialog v-model="openModal">
    <h4 class="modal-text">Зайти как сотрудник<br />или как читатель ?</h4>
    <div class="choice-buttons">
      <StyledButton :disabled="isRoleChanging" @click="handleUserRoleChoice('Reader')"> Читатель </StyledButton>
      <StyledButton :disabled="isRoleChanging" @click="handleUserRoleChoice('Librarian')" theme="accent">
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
import { ref, onMounted, computed } from "vue";

const authStore = useAuthStore();
const userStore = useUserStore();
const { isAuthenticated } = storeToRefs(authStore);
const { currentUser } = storeToRefs(userStore);

//@ts-ignore
const currentRole = computed(() => groups[currentUser.value?.current_role]);

const handleLogout = () => {
  router.push("/");
  authStore.logout();
};

const openModal = ref(false);
const isRoleChanging = ref(false);

onMounted(async () => {
  if (!isAuthenticated.value) {
    return;
  }

  if (!currentUser.value) {
    await userStore.fetchProfile();
  }

  const userRoles = currentUser.value?.groups ?? [];
  const canChooseRole = userRoles.includes("Librarian") || userRoles.includes("Admin");
  openModal.value = canChooseRole && currentUser.value?.current_role === "None";
});

const handleUserRoleChoice = async (choice: Group) => {
  isRoleChanging.value = true;
  const changed = await userStore.setCurrentRole(choice);
  isRoleChanging.value = false;

  if (!changed) {
    return;
  }

  openModal.value = false;

  const role = currentUser.value?.current_role;
  if (role === "Admin") {
    await router.push("/moderator/readers");
  } else if (role === "Librarian") {
    await router.push("/staff/orders");
  } else {
    await router.push("/");
  }

  window.location.reload();
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

.modal-text {
  margin: 0 0 16px;
  color: var(--color-text-700);
  text-align: center;
  line-height: 1.35;
}

.choice-buttons {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 4px 0;
}

.choice-buttons > * {
  min-width: 140px;
}

@media (max-width: 576px) {
  .choice-buttons {
    flex-direction: column;
    gap: 10px;
    width: 100%;
  }

  .choice-buttons > * {
    width: 100%;
  }
}
</style>
