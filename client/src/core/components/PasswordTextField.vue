<template>
  <div class="text-field">
    <TextField
      v-model="model"
      :disabled="disabled"
      :type="showPassword ? 'text' : 'password'"
      :name="name"
      autocomplete="current-password"
      :required="required"
      :readonly="readonly"
      :placeholder="placeholder"
      class="pr-10"
    />
    <button type="button" class="password-button" @click="showPassword = !showPassword">
      <EyeIcon v-if="!showPassword" class="password-icon" />
      <EyeSlashIcon v-else class="password-icon" />
    </button>
  </div>
</template>

<script setup lang="ts">
import TextField from "./TextField.vue";
import { EyeIcon, EyeSlashIcon } from "@heroicons/vue/24/outline";
import { ref } from "vue";

const {
  disabled = false,
  name,
  required,
  readonly,
  placeholder,
} = defineProps<{
  disabled?: boolean;
  name?: string;
  required?: boolean;
  readonly?: boolean;
  placeholder?: string;
}>();

const model = defineModel<string>();

const showPassword = ref(false);
</script>

<style scoped lang="scss">
.text-field {
  position: relative;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.password-button {
  position: absolute;
  right: 0.25rem;

  display: flex;
  flex-direction: row;
  align-items: center;

  background-color: var(--background-color-50);
  color: var(--color-text-950);
  &:hover {
    color: var(--color-text-700);
  }

  border: 0;
  cursor: pointer;
}

.password-icon {
  width: 1.25em;
  height: 1.25em;
}
</style>
