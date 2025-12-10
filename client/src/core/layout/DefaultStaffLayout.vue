<template>
  <div class="app">
    <AppHeader :links="links" />
    <main>
      <div>
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import AppHeader from "@core/components/AppHeader.vue";

import { useStaffLinks } from "@core/composables/useStaffLinks";

const { links } = useStaffLinks();
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
