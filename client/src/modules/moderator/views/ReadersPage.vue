<template>
  <div class="readers-page">
    <div class="page-header">
      <h2>Читатели</h2>
      <div class="stats">
        Всего читателей: {{ readersData.length }}
      </div>
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>#</th>
            <th>ФИО читателя</th>
            <th>Количество заказанных книг</th>
            <th>Количество заказов</th>
            <th>Количество выданных заказов</th>
            <th>Количество отмененных заказов</th>
          </tr>
        </thead>
        <tbody>
          <ReadersTableRow v-for="reader in readersData" :key="reader.id" :reader="reader" />
        </tbody>
      </table>

      <div v-if="readersData.length === 0" class="empty-state">
        Нет данных о читателях
      </div>
    </div>

    <LoadingModal v-model="loading" />
  </div>
</template>

<script setup lang="ts">
import ReadersTableRow from "@modules/moderator/components/ReadersTableRow.vue";
import LoadingModal from "@components/LoadingModal.vue";

import { type Order } from "@api/types";
import { type UserInfo } from "@api/types";

import { ref, onMounted, watch } from "vue";
import { useAuthentication } from "@core/composables/auth";
import { useAuthStore } from "@core/store/auth";
import { useRouter } from "vue-router";

const orders = ref<Order[]>([]);
const readers = ref<UserInfo[]>([])
const loading = ref(false);
const authStore = useAuthStore();
const notAllowedModalOpen = ref(false);
const router = useRouter();

// данные для теста
const readersData = ref([
  {
    id: 1,
    user: {
      first_name: "Иван",
      last_name: "Петров",
      fullname: "Петров Иван Сергеевич",
      username: "i.petrov",
      department: "Институт информационных технологий и анализа данных",
      library_card: "12345"
    },
    total_books_ordered: 15,
    total_orders: 5,
    completed_orders: 3,
    cancelled_orders: 1
  },
  {
    id: 2,
    user: {
      first_name: "Мария",
      last_name: "Сидорова",
      fullname: "Сидорова Мария Ивановна",
      username: "m.sidorova",
      department: "Институт информационных технологий и анализа данных",
      library_card: "12346"
    },
    total_books_ordered: 8,
    total_orders: 3,
    completed_orders: 2,
    cancelled_orders: 0
  },
  {
    id: 3,
    user: {
      first_name: "Алексей",
      last_name: "Кузнецов",
      fullname: "Кузнецов Алексей Петрович",
      username: "a.kuznetsov",
      department: "Институт информационных технологий и анализа данных",
      library_card: "12347"
    },
    total_books_ordered: 22,
    total_orders: 7,
    completed_orders: 5,
    cancelled_orders: 2
  },
  {
    id: 4,
    user: {
      first_name: "Елена",
      last_name: "Васильева",
      fullname: "Васильева Елена Дмитриевна",
      username: "e.vasilyeva",
      department: "Институт информационных технологий и анализа данных",
      library_card: null
    },
    total_books_ordered: 3,
    total_orders: 2,
    completed_orders: 1,
    cancelled_orders: 1
  },
  {
    id: 5,
    user: {
      first_name: "Дмитрий",
      last_name: "Николаев",
      fullname: "Николаев Дмитрий Владимирович",
      username: "d.nikolaev",
      department: "Институт информационных технологий и анализа данных",
      library_card: "12348"
    },
    total_books_ordered: 12,
    total_orders: 4,
    completed_orders: 3,
    cancelled_orders: 0
  }
]);

const loadReadersData = async () => {
  loading.value = true;
  try {
    console.log('Загрузка данных читателей...');
  } catch (error) {
    console.error('Ошибка загрузки данных:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  loadReadersData();
});

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/");
  }
});
</script>

<style scoped lang="scss">
.readers-page {
  flex: 1;
  padding: 16px;
}

.page-header {
  margin-bottom: 1rem;
  
  h2 {
    color: var(--color-text-800);
    margin: 0;
  }
  
  .stats {
    color: var(--color-text-800);
  }
}

.table-container {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 12px;
  text-align: left;
  color: var(--color-text-800);
  background-color: var(--color-background-100);
}

tr {
  border-bottom: 1px solid var(--color-text-200);
}

.empty-state {
  padding: 3rem;
  text-align: center;
  color: var(--color-text-600);
}
</style>