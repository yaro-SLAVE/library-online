<template>
  <input
    type="checkbox"
    :disabled="disabled"
    :name="name"
    :readonly="readonly"
    :checked="checked"
    :value="value"
    v-model="model"
  />
</template>

<script setup lang="ts" generic="T = undefined">
const {
  disabled = false,
  name,
  readonly,
  value,
  checked,
} = defineProps<{
  disabled?: boolean;
  name?: string;
  readonly?: boolean;
  checked?: boolean;
  value?: T;
}>();

const model = defineModel<T extends undefined ? boolean : T[]>();
</script>

<style scoped lang="scss">
input {
  width: 1.35rem;
  height: 1.35rem;
  margin-top: 0.3rem;
  accent-color: var(--color-primary-500);
}
</style>
