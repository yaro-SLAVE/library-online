<template>
  <header>
    <nav class="container">
      <div class="flex flex-row items-center">
        <RouterLink to="/" class="logo-link" active-class="active">
          <span>НТБ ИРНИТУ</span>
          <img :src="Logo" alt="НТБ ИРНИТУ" class="logo" />
        </RouterLink>

        <div class="nav-links">
          <RouterLink
            v-for="[index, link] in props.links.entries()"
            v-bind:key="index"
            :to="link.to"
            class="nav-link"
            active-class="active"
            >{{ link.name }}</RouterLink
          >
        </div>
      </div>

      <div class="nav-end">
        <FontSwitcher />
        <ThemeSwitcher />
        <button class="expand-button" @click="mobileMenuOpen = !mobileMenuOpen">
          <Bars3Icon class="expand-icon nav-link" aria-hidden="true" />
        </button>
      </div>
    </nav>
    <div class="mobile-menu" :class="{ open: mobileMenuOpen }">
      <RouterLink
        v-for="[index, link] in props.links.entries()"
        v-bind:key="index"
        :to="link.to"
        class="nav-link"
        active-class="active"
        >{{ link.name }}</RouterLink
      >
    </div>
  </header>
</template>

<script setup lang="ts">
import Logo from "@assets/images/ntb-logo.png";
import { ref } from "vue";
import { Bars3Icon } from "@heroicons/vue/24/outline";
import FontSwitcher from "@components/FontSwitcher.vue";
import ThemeSwitcher from "@components/ThemeSwitcher.vue";
import type { Link } from "@core/types/types";
interface HeaderProps {
  links: Link[];
}
const props = defineProps<HeaderProps>();

const mobileMenuOpen = ref(false);
</script>

<style scoped lang="scss">
@use "@assets/styles/breakpoints.scss" as *;

header {
  padding-top: 1.25rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid;
  border-color: var(--color-background-100);

  padding-left: 1rem;
  padding-right: 1rem;
  @include media-lg {
    padding-left: 0;
    padding-right: 0;
  }
}

nav {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.nav-end {
  display: flex;
  flex-direction: row;
  align-items: center;
  column-gap: 1rem;
}

.logo-link {
  margin-right: 4rem;
  font-weight: 700;
  text-decoration: none;
  color: var(--color-primary-700);

  &:hover {
    color: var(--color-primary-600);
  }

  &.active {
    color: var(--color-primary-600);
  }
}

// .logo {
//   height: 40px;
// }

.nav-links {
  flex-direction: row;
  align-items: center;
  column-gap: 1rem;

  display: none;
  @include media-lg {
    display: flex;
  }
}

.nav-link {
  text-decoration: none;
  font-weight: 600;
  color: var(--color-text-700);

  &:hover {
    color: var(--color-text-500);
  }

  &.active {
    color: var(--color-text-500);
  }
}

.expand-button {
  background: none;
  border: none;
  cursor: pointer;

  display: block;
  @include media-lg {
    display: none;
  }
}

.expand-icon {
  width: 1.5em;
  height: 1.5em;
}

.mobile-menu {
  flex-direction: column;
  row-gap: 0.5rem;
  padding-top: 1rem;

  display: none;
  &.open {
    display: flex;
  }

  @include media-lg {
    &.open {
      display: none;
    }
  }
}
</style>
