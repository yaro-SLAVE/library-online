<template>
  <div class="switcher">
    <button
      class="switcher-option left"
      :class="{ active: themeStore.font === 'large' }"
      @click="themeStore.setFont('large')"
    >
      A
    </button>
    <button
      class="switcher-option right"
      :class="{ active: themeStore.font === 'standard' }"
      @click="themeStore.setFont('standard')"
    >
      A
    </button>
  </div>
</template>

<script setup lang="ts">
import { useThemeStore } from "@core/store/theme";

const themeStore = useThemeStore();
</script>

<style scoped lang="scss">
@use "@assets/styles/colors.scss" as *;

.switcher {
  width: fit-content;

  background-color: var(--color-background-50);
  color: var(--color-text-950);

  border-style: solid;
  border-radius: 2rem;
  border-width: 1px;
  border-color: var(--color-text-300);

  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);

  display: flex;
  flex-direction: row;
  align-items: stretch;
}

.switcher-option {
  border: 0;
  background-color: var(--color-background-50);
  color: var(--color-text-950);

  cursor: pointer;

  padding: 0.25rem 0.5rem;
  display: flex;
  flex-direction: row;
  align-items: center;

  font-family: "Times New Roman", Times, serif;

  &.left {
    font-size: 1.25em;
    border-top-left-radius: 2rem;
    border-bottom-left-radius: 2rem;
  }

  &.right {
    font-size: 0.75em;
    border-top-right-radius: 2rem;
    border-bottom-right-radius: 2rem;
  }

  transition: 0.05s;
  @include light-theme {
    &:hover,
    &.active {
      background-color: var(--color-background-100);
    }
  }
  @include dark-theme {
    &:hover,
    &.active {
      background-color: var(--color-background-200);
    }
  }
}
</style>
