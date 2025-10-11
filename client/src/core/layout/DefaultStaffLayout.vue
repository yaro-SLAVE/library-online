<template>
  <div class="app">
    <Header :links="links" />
    <main>
      <div>
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { RouterView } from "vue-router";
import { useAuthStore } from "@core/store/auth";
import { useLinksFilter } from "@core/composables/useLinksFilter";
import Header from "@core/components/Header.vue";
import type { LinksConfig } from "@core/types/types";

const authStore = useAuthStore();
const { isAuthenticated } = storeToRefs(authStore);

const rawLinks: LinksConfig[] = [
  {
    to: "/staff/profile",
    name: isAuthenticated.value ? "Профиль" : "Вход",
    hide: false,
  },
  {
    to: "/staff/orders",
    name: "Заказы",
    hide: !isAuthenticated.value,
  },
  {
    to: "/staff/moderator",
    name: "Админка",
    hide: !isAuthenticated.value,
  },
];

const { links } = useLinksFilter(rawLinks);
</script>

<style scoped lang="scss">
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
}

.footer {
  margin-top: 2rem;
}
</style>
