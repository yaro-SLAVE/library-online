<template>
  <div class="table-container">
    <table class="table">
      <thead>
        <tr>
          <th
            @click="sortUsers('library_card')"
            class="sortable-th library-card-column"
            :aria-sort="sortKey === 'library_card' ? (sortOrder === 1 ? 'ascending' : 'descending') : 'none'"
          >
            <span class="th-content">
              Читательский билет
              <div class="th-icon">
                <span v-if="sortKey === 'library_card'" class="direction-icon">
                  {{ sortOrder === 1 ? "↑" : "↓" }}
                </span>
                <span v-else>⇅</span>
              </div>
            </span>
          </th>
          <th
            @click="sortUsers('fullname')"
            class="sortable-th fullname-column"
            :aria-sort="sortKey === 'fullname' ? (sortOrder === 1 ? 'ascending' : 'descending') : 'none'"
          >
            <span class="th-content">
              ФИО
              <div class="th-icon">
                <span v-if="sortKey === 'fullname'" class="direction-icon">
                  {{ sortOrder === 1 ? "↑" : "↓" }}
                </span>
                <span v-else>⇅</span>
              </div>
            </span>
          </th>
          <th class="actions-column">Действия</th>
        </tr>
      </thead>
      <tbody>
        <BlackListTableRow
          v-for="user in sortedUsers"
          :key="user.id"
          :user="user"
          @unban-user="handleUnbanUser"
          :loading="loadingUnbanId === user.id"
        />
      </tbody>
    </table>
    <div v-if="filteredUsers.length === 0" class="empty-state">
      {{ searchQuery ? 'Пользователи по запросу не найдены' : 'Нет заблокированных пользователей' }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import type { BannedUser } from "@api/profile";
import BlackListTableRow from "@moderator/components/BlackListTableRow.vue";

const props = defineProps<{
  users: BannedUser[];
  searchQuery: string;
  loadingUnbanId?: number | null;
}>();

const emit = defineEmits<{
  (e: "unbanUser", userId: number): void;
}>();

type SortKey = "library_card" | "fullname";

const sortKey = ref<SortKey>("library_card");
const sortOrder = ref<1 | -1>(1);

function sortUsers(key: SortKey) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 1 ? -1 : 1;
  } else {
    sortKey.value = key;
    sortOrder.value = 1;
  }
}

// Фильтрация по поисковому запросу
const filteredUsers = computed(() => {
  if (!props.searchQuery.trim()) {
    return props.users;
  }
  
  const searchTerm = props.searchQuery.toLowerCase().trim();
  return props.users.filter(user => 
    user.fullname?.toLowerCase().includes(searchTerm) ||
    user.library_card?.toLowerCase().includes(searchTerm)
  );
});

// Сортировка
const sortedUsers = computed(() => {
  if (!filteredUsers.value) return [];

  return [...filteredUsers.value].sort((a, b) => {
    let comparison = 0;

    switch (sortKey.value) {
      case "fullname":
        const aName = a.fullname?.toLowerCase() || '';
        const bName = b.fullname?.toLowerCase() || '';
        comparison = aName.localeCompare(bName);
        break;
      case "library_card":
      default:
        const aCard = a.library_card?.toLowerCase() || '';
        const bCard = b.library_card?.toLowerCase() || '';
        comparison = aCard.localeCompare(bCard);
    }

    return comparison * sortOrder.value;
  });
});

const handleUnbanUser = (userId: number) => {
  emit("unbanUser", userId);
};
</script>

<style scoped lang="scss">
.table-container {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  min-width: 320px; /* Минимальная ширина для мобильных */
  background-color: var(--color-background-100);
}

th,
td {
  padding: 12px 8px;
  text-align: left;
  color: var(--color-text-800);
  background-color: var(--color-background-100);
  
  @media (max-width: 768px) {
    padding: 10px 6px;
    font-size: 0.9em;
  }
  
  @media (max-width: 480px) {
    padding: 8px 4px;
    font-size: 0.85em;
  }
}

tr {
  border-bottom: 1px solid var(--color-text-200);
}

/* Ширины колонок */
.library-card-column {
  width: 20%; /* Уменьшили с ~25% до 20% */
  min-width: 100px;
  
  @media (max-width: 768px) {
    width: 22%;
    min-width: 90px;
  }
  
  @media (max-width: 480px) {
    width: 25%;
    min-width: 80px;
  }
}

.actions-column {
  width: 18%; /* Уменьшили для баланса */
  min-width: 100px;
  
  @media (max-width: 768px) {
    width: 20%;
    min-width: 90px;
  }
  
  @media (max-width: 480px) {
    width: 22%;
    min-width: 80px;
  }
}

.fullname-column {
  width: auto; /* Занимает оставшееся пространство */
  min-width: 120px;
}

.sortable-th {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;

  &:hover {
    background-color: var(--color-background-200);

    .th-icon {
      opacity: 1;
    }
  }

  &[aria-sort="ascending"],
  &[aria-sort="descending"] {
    .th-icon {
      opacity: 1;
      font-weight: bold;
    }
  }
}

.th-content {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
  
  @media (max-width: 480px) {
    gap: 2px;
  }
}

.th-icon {
  font-size: 0.9em;
  opacity: 0.7;
  transition: opacity 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1em;
  height: 1em;
  
  @media (max-width: 480px) {
    font-size: 0.8em;
  }
}

.direction-icon {
  font-weight: bold;
  color: var(--color-primary-500);
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--color-text-600);
  font-size: 1.1em;
  background-color: var(--color-background-100);
  
  @media (max-width: 768px) {
    padding: 30px 20px;
    font-size: 1em;
  }
}
</style>