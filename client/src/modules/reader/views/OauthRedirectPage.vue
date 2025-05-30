<template>
  <div class="text-center">
    <h1>
      {{ states[state] }}
    </h1>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "@core/store/auth";
import { onBeforeMount, ref } from "vue";
import { useRouter } from "vue-router";

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
      state.value = "success";
      router.push("/profile");
    } else {
      state.value = "error";
    }
  } else {
    state.value = "error";
  }
});
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
