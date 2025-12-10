<template>
  <input
    v-model="model"
    :name="name"
    :type="type"
    :autocomplete="autocomplete"
    :required="required"
    :readonly="readonly"
    :placeholder="placeholder"
    :disabled="disabled"
  />
</template>

<script setup lang="ts">
import { type InputTypeHTMLAttribute } from "vue";

const {
  disabled = false,
  type = "text",
  name,
  autocomplete,
  required,
  readonly,
  placeholder,
} = defineProps<{
  disabled?: boolean;
  type?: InputTypeHTMLAttribute;
  name?: string;
  autocomplete?: string;
  required?: boolean;
  readonly?: boolean;
  placeholder?: string;
}>();

const model = defineModel<string>();
</script>

<style scoped lang="scss">
input {
  display: block;
  width: 100%;

  background-color: var(--color-background-50);
  color: var(--color-text-950);
  &::placeholder {
    color: var(--color-text-300);
  }

  padding: 0.5rem 0.75rem;

  border-style: solid;
  border-radius: 0.5rem;
  border-width: 1px;
  border-color: var(--color-text-300);

  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
