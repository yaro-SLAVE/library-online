<template>
  <div class="search-container">
    <div class="search-input-wrapper">
      <input
        v-model="searchValue"
        type="text"
        placeholder="Поиск по ФИО..."
        class="search-input"
        @input="handleInput"
      />
      <span class="clear-search" v-if="searchValue" @click="clearSearch">
        ×
      </span>
    </div>
    <div class="search-counter" v-if="searchValue && itemCount !== undefined">
      Найдено: {{ itemCount }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps<{
  modelValue: string;
  itemCount?: number;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();

const searchValue = ref(props.modelValue);

watch(() => props.modelValue, (newValue) => {
  searchValue.value = newValue;
});

const handleInput = () => {
  emit("update:modelValue", searchValue.value);
};

const clearSearch = () => {
  searchValue.value = '';
  emit("update:modelValue", '');
};
</script>

<style scoped lang="scss">
.search-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
}

.search-input-wrapper {
  position: relative;
  flex: 1;
  max-width: 400px;
  
  @media (max-width: 768px) {
    max-width: none;
  }
}

.search-input {
  width: 100%;
  padding: 10px 35px 10px 12px;
  border: 1px solid var(--color-text-200);
  border-radius: 6px;
  font-size: 14px;
  background-color: var(--color-background-100);
  color: var(--color-text-800);
  transition: 
    border-color 0.2s ease,
    box-shadow 0.2s ease;

  &:focus {
    outline: none;
    border-color: var(--color-primary-400);
    box-shadow: 0 0 0 2px rgba(var(--color-primary-400-rgb), 0.1);
  }

  &::placeholder {
    color: var(--color-text-400);
  }
}

.clear-search {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: var(--color-text-400);
  font-size: 18px;
  font-weight: bold;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;

  &:hover {
    background-color: var(--color-background-200);
    color: var(--color-text-600);
  }
}

.search-counter {
  color: var(--color-text-600);
  font-size: 0.9em;
  white-space: nowrap;
  
  @media (max-width: 768px) {
    text-align: center;
  }
}
</style>