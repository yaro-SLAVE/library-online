<template>
  <div class="surface">
    <slot></slot>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped lang="scss">
@use "@assets/styles/breakpoints.scss" as *;

.surface {
  background-color: var(--color-background-100);
  color: var(--color-text-900);

  border-radius: 1rem;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);

  padding: 1rem;
  @include media-lg {
    padding: 1rem 4rem;
  }
}
</style>
