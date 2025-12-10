<template>
  <div class="switcher">
    <button
      class="switcher-option left"
      :class="{ active: themeStore.theme === 'light' }"
      @click="themeStore.setTheme('light')"
    >
      <SunIcon class="switcher-icon" />
    </button>
    <button
      class="switcher-option"
      :class="{ active: themeStore.theme === 'system' }"
      @click="themeStore.setTheme('system')"
    >
      <ComputerDesktopIcon class="switcher-icon" />
    </button>
    <button
      class="switcher-option right"
      :class="{ active: themeStore.theme === 'dark' }"
      @click="themeStore.setTheme('dark')"
    >
      <MoonIcon class="switcher-icon" />
    </button>
  </div>
</template>

<script setup lang="ts">
import { useThemeStore } from "@core/store/theme";
import { SunIcon, MoonIcon, ComputerDesktopIcon } from "@heroicons/vue/24/outline";

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
  align-items: center;
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

  &.left {
    border-top-left-radius: 2rem;
    border-bottom-left-radius: 2rem;
  }

  &.right {
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

.switcher-icon {
  width: 1.25em;
  height: 1.25em;
}
</style>
