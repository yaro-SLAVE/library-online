<template>
  <div v-if="open" @click="open &&= !escCloseable" class="modal-overlay">
    <div class="modal-dialog" @click.stop>
      <div class="modal-content">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { watch } from "vue";

const { escCloseable = true } = defineProps<{
  escCloseable?: boolean;
}>();
const open = defineModel<boolean>({ required: true });

function keydownClose(event: KeyboardEvent) {
  if (event.key === "Escape") {
    open.value = false;
  }
}

watch(
  open,
  () => {
    if (open.value && escCloseable) {
      document.addEventListener("keydown", keydownClose);
      console.log("add");
    } else {
      document.removeEventListener("keydown", keydownClose);
      console.log("remove");
    }
  },
  {
    immediate: true,
  }
);
</script>

<style scoped lang="scss">
.modal-overlay {
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;

  background: rgba(0, 0, 0, 0.5);
}

.modal-dialog {
  position: relative;
  margin: 10vh auto;
  max-width: fit-content;

  padding: 1rem;
  border-radius: 1rem;

  background: var(--color-background-50);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);

  max-height: 85vh;
  overflow-y: auto;
}
</style>
