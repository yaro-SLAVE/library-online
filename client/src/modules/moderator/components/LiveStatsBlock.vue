<script setup lang="ts">
import type { LiveStats } from "@core/api/types";
import { NewspaperIcon, HandRaisedIcon, CheckIcon, EyeIcon } from "@heroicons/vue/24/outline";
const props = defineProps<LiveStats>();

const statsConfig = [
  {
    key: "new_orders",
    label: "Новые заказы",
    color: "var(--color-primary-400)",
    icon: NewspaperIcon,
    gradient: "linear-gradient(135deg, var(--color-primary-300), var(--color-primary-500))",
  },
  {
    key: "orders_in_work",
    label: "В работе",
    color: "var(--color-primary-500)",
    icon: EyeIcon,
    gradient: "linear-gradient(135deg, var(--color-primary-400), var(--color-primary-600))",
  },
  {
    key: "orders_in_waiting",
    label: "В ожидании",
    color: "var(--color-primary-600)",
    icon: HandRaisedIcon,
    gradient: "linear-gradient(135deg, var(--color-primary-500), var(--color-primary-700))",
  },
  {
    key: "done_today",
    label: "Собрали сегодня",
    color: "var(--color-primary-700)",
    icon: CheckIcon,
    gradient: "linear-gradient(135deg, var(--color-primary-600), var(--color-primary-800))",
  },
];
</script>

<template>
  <div class="live-stats-grid">
    <div
      v-for="stat in statsConfig"
      :key="stat.key"
      class="stat-card"
      :style="{ '--card-color': stat.color, '--card-gradient': stat.gradient }"
    >
      <component :is="stat.icon" class="stat-icon" />
      <div class="stat-content">
        <div class="stat-value">{{ (props as any)[stat.key] }}</div>
        <div class="stat-label">{{ stat.label }}</div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.live-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
}

.stat-card {
  background-color: var(--color-background-100);
  border-radius: 16px;
  box-shadow: 0 2px 6px rgba(157, 98, 123, 0.15);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-4px);
  }

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--card-gradient);
  }
}

.stat-icon {
  max-width: 50px;
  font-size: 1.5rem;
  z-index: 1;
  color: var(--card-color);
  position: relative;
}

.stat-content {
  z-index: 1;
  position: relative;
  flex: 1;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--card-color);
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-label {
  color: var(--card-color);
  font-size: 0.95rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .live-stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    padding: 0.5rem;
  }

  .stat-card {
    padding: 1.25rem;
    gap: 1rem;
  }

  .stat-value {
    font-size: 2rem;
  }

  .stat-icon {
    font-size: 2rem;
  }
}
</style>
