<template>
  <div class="app">
    <AppHeader :links="links" />
    <main>
      <ModeratorSideBar :links="sidebarLinks" />
      <RouterView />      

    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import AppHeader from "@core/components/AppHeader.vue";
import ModeratorSideBar from "./ModeratorSideBar.vue";
import { useModeratorLinks } from "@core/composables/useModeratorLinks";
import { sidebarLinks } from "./sidebarData";

const { links } = useModeratorLinks();
</script>

<style scoped lang="scss">
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
  display: flex;
  flex-direction: row;
  gap: 2rem;
}

.footer {
  margin-top: 2rem;
}
</style>
