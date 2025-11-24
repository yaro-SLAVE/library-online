<template>
  <div class="tabs-container">
    <ul class="tabs">
      <li class="tab-item">
        <a
          class="tab-link"
          :class="{ active: currentTab === tabsNumbers.new }"
          @click="currentTab = tabsNumbers.new"
          href="#"
        >
          Новые <span class="badge">{{ newOrdersCount }}</span>
        </a>
      </li>
      <li class="tab-item">
        <a
          class="tab-link"
          :class="{ active: currentTab === tabsNumbers.processing }"
          @click="currentTab = tabsNumbers.processing"
          href="#"
        >
          В работе <span class="badge">{{ processingOrdersCount }}</span>
        </a>
      </li>
      <li class="tab-item">
        <a
          class="tab-link"
          :class="{ active: currentTab === tabsNumbers.ready }"
          @click="currentTab = tabsNumbers.ready"
          href="#"
        >
          Готовые к выдаче <span class="badge">{{ readyOrdersCount }}</span>
        </a>
      </li>
      <li class="tab-item">
        <a
          class="tab-link"
          :class="{ active: currentTab === tabsNumbers.archive }"
          @click="currentTab = tabsNumbers.archive"
          href="#"
        >
          Архив <span class="badge">{{ archiveOrdersCount }}</span>
        </a>
      </li>
    </ul>
    <OrderList @get-order="fetchOrder" :orders="currentData" />
    <ModalOrderDetails
      v-if="selectedOrder"
      :order="selectedOrder"
      :onCheckOrder="handleCheckOrder"
      @close="selectedOrder = null"
      @next-order-status="handleUpdateOrderStatus"
    />
    <LoadingModal v-model="isLoading" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useUserStore } from "@core/store/user";
import LoadingModal from "@components/LoadingModal.vue";
import OrderList from "@staff/components/OrderList.vue";
import ModalOrderDetails from "@staff/components/ModalOrderDetails.vue";

import {
  fetchNewOrders,
  fetchProcessingOrders,
  fetchReadyOrders,
  fetchArchiveOrders,
} from "@api/order";

import type { UserOrder, Order, OrderStatusEnum, OrderCheckingInfo } from "@api/types";
import { getOrderStaff, updateOrderStatus, checkOrder } from "@api/order";

const userStore = useUserStore();
const isLoading = ref(false);

interface TabConfig {
  label: string;
  fetchFn: () => Promise<UserOrder[]>;
  interval: number;
  data: UserOrder[];
  timerId?: number;
}

const tabsNumbers = {
  new: 0,
  processing: 1,
  ready: 2,
  archive: 3,
};

const currentTab = ref(tabsNumbers.new);

const tabs = ref<TabConfig[]>([
  {
    label: "Новые",
    fetchFn: fetchNewOrders,
    interval: 3000,
    data: [],
  },
  {
    label: "В работе",
    fetchFn: fetchProcessingOrders,
    interval: 3000,
    data: [],
  },
  {
    label: "Готовые",
    fetchFn: fetchReadyOrders,
    interval: 3000,
    data: [],
  },
  {
    label: "Архив",
    fetchFn: fetchArchiveOrders,
    interval: 10000,
    data: [],
  },
]);

const newOrdersCount = computed(() => tabs.value[tabsNumbers.new].data.length);
const processingOrdersCount = computed(() => tabs.value[tabsNumbers.processing].data.length);
const readyOrdersCount = computed(() => tabs.value[tabsNumbers.ready].data.length);
const archiveOrdersCount = computed(() => tabs.value[tabsNumbers.archive].data.length);
const selectedOrder = ref<Order | null>(null);
const startAllIntervals = () => {
  tabs.value.forEach((tab, index) => {
    tab.timerId = window.setInterval(async () => {
      if (document.visibilityState === "visible") {
        try {
          tabs.value[index].data = await fetchUserOrders(tab);
        } catch (error) {
          console.error(`Ошибка обновления вкладки ${tab.label}:`, error);
        }
      }
    }, tab.interval);

    tab.fetchFn().then(async () => {
      tabs.value[index].data = await fetchUserOrders(tab);
    });
  });
};

//TODO: Разобраться с тем, что есть в бэке, и что есть на фронте для проверки показа только закрепленных за сотрудником заказов
const fetchUserOrders = async (tab: TabConfig): Promise<UserOrder[]> => {
  let data = await tab.fetchFn();
  if (tab.label === "В работе") {
    data = data.filter((order) => {
      let name = "";
      order.statuses.forEach((status) => {
        if (status.status === "processing") {
          name = status.staff.username;
        }
      });
      return name === userStore.currentUser?.username;
    });
  }
  return data;
};

const clearAllIntervals = () => {
  tabs.value.forEach((tab) => {
    if (tab.timerId) {
      clearInterval(tab.timerId);
    }
  });
};

const currentData = computed<UserOrder[]>((): UserOrder[] => {
  switch (currentTab.value) {
    case tabsNumbers.new:
      return tabs.value[tabsNumbers.new].data;
    case tabsNumbers.processing:
      return tabs.value[tabsNumbers.processing].data;
    case tabsNumbers.ready:
      return tabs.value[tabsNumbers.ready].data;
    case tabsNumbers.archive:
      return tabs.value[tabsNumbers.archive].data;
    default:
      return [];
  }
});

const fetchOrder = async (orderId: number) => {
  isLoading.value = true;
  selectedOrder.value = await getOrderStaff(orderId);

  isLoading.value = false;
};

async function handleUpdateOrderStatus(
  orderId: number,
  newStatus: OrderStatusEnum,
  description: string,
  books: [] = []
) {
  try {
    await updateOrderStatus(orderId, newStatus, description, books);
  } catch (error) {
    console.error("Ошибка при обновлении статуса заказа", error);
  }
}

async function handleCheckOrder(orderId: number): Promise<OrderCheckingInfo | undefined> {
  try {
    return await checkOrder(orderId);
  } catch (error) {
    console.error("Ошибка при проверке готовности заказа", error);
  }
}

onMounted(async () => {
  startAllIntervals();
});

onUnmounted(() => {
  clearAllIntervals();
});

document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "hidden") {
    clearAllIntervals();
  } else {
    startAllIntervals();
  }
});
</script>

<style lang="scss" scoped>
.tabs-container {
  padding: 16px;
}

.tabs {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
  border-bottom: 2px solid #ddd;
}

.tab-item {
  margin-right: 16px;
}

.tab-link {
  text-decoration: none;
  color: var(--color-text-800);
  padding: 10px 15px;
  font-weight: 500;
  border-radius: 5px;
  display: inline-block;
}

.tab-link.active {
  background-color: var(--color-background-100);
}

.badge {
  background-color: var(--color-primary-400);
  color: var(--color-text-50);
  padding: 5px 10px;
  border-radius: 20%;
  font-size: 0.9em;
  margin-left: 5px;
}
</style>
