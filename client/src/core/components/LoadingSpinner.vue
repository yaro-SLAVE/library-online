<template>
  <div class="loader"></div>
</template>

<style scoped lang="scss">
.loader {
  width: 2em;
  height: 2em;
  border: 0.25em dotted var(--color-text-950);
  border-radius: 50%;
  display: inline-block;
  position: relative;
  box-sizing: border-box;
  animation: rotation 2s linear infinite;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
