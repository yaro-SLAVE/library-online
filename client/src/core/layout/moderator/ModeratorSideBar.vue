<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { motion, useDomRef, type MotionProps } from "motion-v";
import { Bars3Icon, XMarkIcon } from "@heroicons/vue/24/outline";
import type { SidebarLink } from "@core/types/types";

interface SidebarProps {
  links: SidebarLink[];
}
const props = defineProps<SidebarProps>();

const isOpen = ref(false);
const containerRef = useDomRef();
const dimensions = ref({ width: 0, height: 0 });

onMounted(() => {
  if (containerRef.value) {
    dimensions.value.width = containerRef.value.offsetWidth;
    dimensions.value.height = containerRef.value.offsetHeight;
  }
});

const currentBarIcon = computed(() => {
  return isOpen.value ? XMarkIcon : Bars3Icon;
});

const toggle = () => {
  isOpen.value = !isOpen.value;
};

const itemVariants = {
  open: {
    y: 0,
    opacity: 1,
    transition: {
      y: { stiffness: 1000, velocity: -100 },
    },
  },
  closed: {
    y: 50,
    opacity: 0,
    transition: {
      y: { stiffness: 1000 },
    },
  },
};

const sidebarVariants: MotionProps["variants"] = {
  open: {
    x: 0,
    width: "260px",
    transition: {
      type: "spring",
      stiffness: 200,
      damping: 25,
    },
  },
  closed: {
    width: "0px",
    padding: "0px",
    x: "-100%",
    transition: {
      type: "spring",
      stiffness: 200,
      damping: 25,
    },
  },
};
</script>

<template>
  <div class="container">
    <motion.nav
      :initial="false"
      :animate="isOpen ? 'open' : 'closed'"
      :custom="dimensions.height"
      :class="{ 'nav--open': isOpen }"
      ref="containerRef"
      class="nav"
    >
      <button class="toggle-container" @click="toggle">
        <component :is="currentBarIcon" class="toggle-icon" />
      </button>
      <motion.ul class="list" :variants="sidebarVariants" v-show="isOpen || true">
        <motion.li
          v-for="link in props.links"
          :key="link.name"
          class="list-item"
          :variants="itemVariants"
          :whileHover="{ scale: 1.25 }"
        >
          <div class="icon-placeholder">
            <component :is="link.icon" class="icon-placeholder" />
          </div>

          <RouterLink :to="{ name: link.to }" class="text-placeholder">
            {{ link.name }}
          </RouterLink>
        </motion.li>
      </motion.ul>
    </motion.nav>
  </div>
</template>

<style scoped>
.container {
  flex: 1;
  max-width: fit-content;
  background-color: none;
  backdrop-filter: blur(30px);
}

.nav {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  height: 100vh;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  background-color: none;
}

.nav--open {
  border-right: 1px solid var(--color-text-700);
}

.toggle-container {
  margin-top: 1rem;
  margin-left: 1rem;
  margin-bottom: 1rem;
  max-width: fit-content;
  max-height: fit-content;
  background-color: var(--color-background-100);
  color: var(--color-text-400);
  border: none;
}

.toggle-icon {
  border-radius: 30px;
  width: 30px;
  height: 30px;
  color: var(--color-text-700);
  background-color: var(--color-background-100);
  transition: transform 0.2s ease-in-out;
}

.list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  margin: 0;
  width: 100%;
  list-style: none;
  scrollbar-width: thin;
  scrollbar-color: var(--color-background-300) transparent;
}

.list::-webkit-scrollbar {
  width: 6px;
}

.list::-webkit-scrollbar-thumb {
  background-color: var(--color-background-300);
  border-radius: 3px;
}

.list::-webkit-scrollbar-thumb:hover {
  background-color: var(--color-background-400);
}

.list-item {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin: 0;
  padding: 3px;
  border-radius: 1rem;
  list-style: none;
  margin-bottom: 20px;
  cursor: pointer;
}

.list-item:hover {
  background-color: var(--color-background-200);
}

.icon-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  flex: 40px 0;
  margin-right: 20px;
  color: var(--color-text-700);
}

.text-placeholder {
  flex: 1;
  text-decoration: none;
  font-weight: 500;
  color: var(--color-text-700);
  border-bottom: 1px solid;
}
</style>
