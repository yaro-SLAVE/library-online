<template>
  <button :disabled="disabled" :type="type" :class="theme">
    <div class="flex flex-row items-center justify-center">
      <slot>Button</slot>
    </div>
  </button>
</template>

<script setup lang="ts">
import { type ButtonHTMLAttributes } from "vue";

const {
  disabled = false,
  type = "button",
  theme = "primary",
} = defineProps<{
  disabled?: boolean;
  type?: ButtonHTMLAttributes["type"];
  theme?: "primary" | "secondary" | "accent";
}>();
</script>

<style scoped lang="scss">
@use "@assets/styles/colors.scss" as *;

button {
  border-radius: 0.5rem;
  border: none;

  padding-left: 2rem;
  padding-right: 2rem;
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;

  font-size: var(--text-sm);
  font-weight: 500;

  transition: 0.05s;
  cursor: pointer;
  &:disabled {
    cursor: default;
  }

  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);

  &.primary {
    background-color: var(--color-primary-500);
    &:hover {
      background-color: var(--color-primary-600);
    }
    &:disabled {
      background-color: var(--color-primary-100);
    }

    @include light-theme {
      color: var(--color-text-50);
      &:disabled {
        color: var(--color-text-300);
      }
    }
    @include dark-theme {
      color: var(--color-text-950);
      &:disabled {
        color: var(--color-text-300);
      }
    }
  }

  &.secondary {
    background-color: var(--color-secondary-200);
    color: var(--color-text-950);
    &:hover {
      background-color: var(--color-secondary-300);
    }
    &:disabled {
      color: var(--color-text-300);
      background-color: var(--color-secondary-100);
    }
  }

  &.accent {
    background-color: var(--color-accent-500);
    &:hover {
      background-color: var(--color-accent-600);
    }
    &:disabled {
      background-color: var(--color-accent-100);
    }

    @include light-theme {
      color: var(--color-text-50);
      &:disabled {
        color: var(--color-text-300);
      }
    }
    @include dark-theme {
      color: var(--color-text-900);
      &:disabled {
        color: var(--color-text-300);
      }
    }
  }
}
</style>
