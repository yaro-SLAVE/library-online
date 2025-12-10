<template>
  <select v-model="model">
    <option v-if="blankOption" :value="undefined">
      {{ typeof blankOption === "string" ? blankOption : "" }}
    </option>
    <option v-for="option in options" v-bind:key="option.id" :value="option.id">
      {{ option.name }}
    </option>
  </select>
</template>

<script setup lang="ts" generic="Id extends PropertyKey, Blank extends string | boolean = false">
import { watch } from "vue";

export type SelectModel<
  Id extends PropertyKey,
  Blank extends string | boolean,
> = Blank extends false ? Id : Id | undefined;

const { options, defaultOption, blankOption } = defineProps<{
  options: readonly { id: Id; name: string }[];
  defaultOption?: Id;
  blankOption?: Blank;
}>();

const model = defineModel<SelectModel<Id, Blank>>();

watch(
  () => defaultOption,
  (value) => {
    model.value = value;
  },
  {
    immediate: true,
  }
);
</script>

<style scoped lang="scss">
select {
  background-color: var(--color-background-50);
  color: var(--color-text-950);

  transition: 0.05s;
  &:hover {
    background-color: var(--color-background-100);
  }

  padding: 0.5rem 0.75rem;
  cursor: pointer;

  border-style: solid;
  border-radius: 0.5rem;
  border-width: 1px;
  border-color: var(--color-text-300);

  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
