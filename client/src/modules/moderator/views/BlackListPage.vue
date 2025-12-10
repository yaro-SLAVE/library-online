<template>
  <div class="tabs-container">
    <ul class="tabs">
      <li class="tab-item">
        <a
          class="tab-link"
          :class="{ active: currentTab === tabsNumbers.candidates }"
          @click="currentTab = tabsNumbers.candidates"
          href="#"
        >
          Претенденты на блокировку
        </a>
      </li>
      <li class="tab-item">
        <a
          class="tab-link"
          :class="{ active: currentTab === tabsNumbers.banned }"
          @click="currentTab = tabsNumbers.banned"
          href="#"
        >
          Заблокированные читатели
        </a>
      </li>
    </ul>

    <!-- Претенденты на блокировку -->
    <div v-if="currentTab === tabsNumbers.candidates" class="tab-content">
      <!-- Фильтр по датам для запроса к бэкенду -->
      <DateFilter 
        :loading="loadingCandidates"
        @search="handleCandidatesSearch"
        @initial-dates="handleInitialDates"
      />
      
      <!-- Поиск по уже полученному списку -->
      <SearchInput 
        v-model="candidatesSearchQuery"
        :item-count="filteredCandidates.length"
      />
      
      <!-- Таблица с уже отфильтрованными данными -->
      <BanCandidatesTable
        :candidates="filteredCandidates"
        :loading="loadingCandidates"
        :loading-ban-id="banningUserId"
        :has-searched="hasSearchedCandidates"
        @ban-user="handleBanCandidate"
      />
    </div>

    <!-- Заблокированные читатели -->
    <div v-else-if="currentTab === tabsNumbers.banned" class="tab-content">
      <SearchInput 
        v-model="bannedSearchQuery" 
        :item-count="filteredBannedUsers.length"
      />
      
      <BlackListTable
        :users="bannedUsers"
        :search-query="bannedSearchQuery"
        :loading-unban-id="unbanningUserId"
        @unban-user="handleUnbanUser"
      />
    </div>

    <LoadingModal v-model="isLoading" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import LoadingModal from "@components/LoadingModal.vue";
import SearchInput from "@moderator/components/SearchInput.vue";
import BlackListTable from "@moderator/components/BlackListTable.vue";
import DateFilter from "@moderator/components/DateFilter.vue";
import BanCandidatesTable from "@moderator/components/BanCandidatesTable.vue";
import { 
  fetchBannedUsers, 
  unbanUser, 
  fetchBanCandidates, 
  banUser,
  type BannedUser,
  type BanCandidate 
} from "@api/profile";

const router = useRouter();
const isLoading = ref(false);
const unbanningUserId = ref<number | null>(null);
const banningUserId = ref<number | null>(null);

// Поисковые запросы
const bannedSearchQuery = ref('');
const candidatesSearchQuery = ref('');

const tabsNumbers = {
  candidates: 0,
  banned: 1,
};

const currentTab = ref(tabsNumbers.candidates);

// Данные для заблокированных пользователей
const bannedUsers = ref<BannedUser[]>([]);
const loadingBanned = ref(false);

// Данные для кандидатов на блокировку
const candidates = ref<BanCandidate[]>([]);
const loadingCandidates = ref(false);
const hasSearchedCandidates = ref(false);

// Фильтрация заблокированных пользователей на клиенте
const filteredBannedUsers = computed(() => {
  if (!bannedSearchQuery.value.trim()) {
    return bannedUsers.value;
  }
  
  const searchTerm = bannedSearchQuery.value.toLowerCase().trim();
  return bannedUsers.value.filter(user => 
    user.fullname?.toLowerCase().includes(searchTerm) ||
    user.library_card?.toLowerCase().includes(searchTerm)
  );
});

// Фильтрация кандидатов на клиенте
const filteredCandidates = computed(() => {
  if (!candidatesSearchQuery.value.trim()) {
    return candidates.value;
  }
  
  const searchTerm = candidatesSearchQuery.value.toLowerCase().trim();
  return candidates.value.filter(candidate => 
    candidate.fullname?.toLowerCase().includes(searchTerm) ||
    candidate.library_card?.toLowerCase().includes(searchTerm)
  );
});

// Обработчик начальных дат (автоматический запрос при загрузке)
const handleInitialDates = (startDate: string, endDate: string) => {
  if (!hasSearchedCandidates.value) {
    handleCandidatesSearch(startDate, endDate);
  }
};

// Загрузка кандидатов на блокировку (только даты идут в запрос)
const handleCandidatesSearch = async (startDate: string, endDate: string) => {
  loadingCandidates.value = true;
  hasSearchedCandidates.value = true;
  
  try {
    console.log('Запрос кандидатов с датами:', startDate, 'до', endDate);
    
    // Запрос к бэкенду с датами
    const result = await fetchBanCandidates(startDate, endDate);
    console.log('Получены кандидаты:', result);
    
    candidates.value = result;
  } catch (error: any) {
    console.error('Ошибка при получении кандидатов на блокировку:', error);
    
    if (error.response?.status === 401) {
      router.push('/login');
    }
  } finally {
    loadingCandidates.value = false;
  }
};

// Блокировка кандидата
const handleBanCandidate = async (userId: number) => {
  banningUserId.value = userId;
  
  try {
    await banUser(userId);
    
    // Удаляем кандидата из списка после успешной блокировки
    candidates.value = candidates.value.filter(candidate => candidate.user_id !== userId);
    
    // Обновляем список заблокированных пользователей
    await loadBannedUsers();
    
    console.log(`Пользователь ${userId} успешно заблокирован`);
    
  } catch (error: any) {
    console.error('Ошибка при блокировке пользователя:', error);
    
    if (error.response?.status === 401) {
      router.push('/login');
    }
  } finally {
    banningUserId.value = null;
  }
};

// Загрузка данных о заблокированных пользователях
const loadBannedUsers = async () => {
  loadingBanned.value = true;
  try {
    bannedUsers.value = await fetchBannedUsers();
  } catch (error: any) {
    console.error('Ошибка при получении списка забаненных пользователей:', error);
    
    if (error.response?.status === 401) {
      router.push('/login');
    }
  } finally {
    loadingBanned.value = false;
  }
};

// Функция для разблокировки пользователя
const handleUnbanUser = async (userId: number) => {
  unbanningUserId.value = userId;
  try {
    await unbanUser(userId);
    
    bannedUsers.value = bannedUsers.value.filter(user => user.id !== userId);
    console.log(`Пользователь ${userId} успешно разблокирован`);
    
  } catch (error: any) {
    console.error('Ошибка при разблокировке пользователя:', error);
    
    if (error.response?.status === 401) {
      router.push('/login');
    }
  } finally {
    unbanningUserId.value = null;
  }
};

onMounted(async () => {
  await loadBannedUsers();
});
</script>

<style lang="scss" scoped>
.tabs-container {
  padding: 16px;
  background-color: var(--color-background-50);
}

.tabs {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
  border-bottom: 2px solid var(--color-text-200);
  background-color: var(--color-background-100);
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
  transition: background-color 0.2s ease;
  background-color: var(--color-background-100);

  &:hover {
    background-color: var(--color-background-200);
  }
}

.tab-link.active {
  background-color: var(--color-primary-400);
  color: var(--color-text-50);
}

.tab-content {
  min-height: 400px;
  background-color: var(--color-background-50);
}
</style>