<template>
  <div class="app">
    <Header :links="links" />
    <main>
        <ModeratorSideBar :links="sidebarLinks"/>
        <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import Header from "@core/components/Header.vue";
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
}

.footer {
  margin-top: 2rem;
}
</style>