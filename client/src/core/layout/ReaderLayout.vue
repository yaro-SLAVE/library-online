<template>
  <div class="app">
    <Header :links="links"/>
    <PageHeader/>
    <main>
      <div>
        <RouterView />
      </div>
    </main>
  </div>

  <PageFooter class="footer" />
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import Header from "@core/components/Header.vue";
import PageFooter from "@reader/components/PageFooter.vue";
import { useReaderLinks } from "@core/composables/useReaderLinks";

const { links } = useReaderLinks();
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
