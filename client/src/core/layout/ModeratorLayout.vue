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
import { RouterView } from "vue-router";
import Header from "@core/components/Header.vue";

import { useModeratorLinks } from "@core/composables/useModeratorLinks";
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
}

.footer {
  margin-top: 2rem;
}
</style>