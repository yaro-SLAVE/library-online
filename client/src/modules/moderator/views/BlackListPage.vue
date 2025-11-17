<template>
  <div class="banned-users-container">
    <h2>Заблокированные пользователи</h2>
    
    <div v-if="isLoading" class="loading">
      Загрузка...
    </div>
    
    <div v-else-if="bannedUsers.length === 0" class="empty-state">
      Нет заблокированных пользователей
    </div>
    
    <div v-else class="users-list">
      <div 
        v-for="user in bannedUsers" 
        :key="user.id" 
        class="user-item"
      >
        <span class="username">{{ user.username }}</span>
        <button 
          class="unban-btn"
          @click="handleUnbanUser(user.id)"
          :disabled="unbanningUserId === user.id"
        >
          <span v-if="unbanningUserId === user.id">Разблокировка...</span>
          <span v-else>Разблокировать</span>
        </button>
      </div>
    </div>

    <LoadingModal v-model="isLoading" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import LoadingModal from "@components/LoadingModal.vue";
import { fetchBannedUsers, unbanUser, type BannedUser } from "@api/profile";

const router = useRouter();
const bannedUsers = ref<BannedUser[]>([]);
const isLoading = ref(false);
const unbanningUserId = ref<number | null>(null);

// Функция для получения списка забаненных пользователей
const loadBannedUsers = async () => {
  isLoading.value = true;
  try {
    bannedUsers.value = await fetchBannedUsers();
  } catch (error: any) {
    console.error('Ошибка при получении списка забаненных пользователей:', error);
    
    // Обрабатываем ошибку авторизации
    if (error.response?.status === 401) {
      console.log('Пользователь не авторизован, перенаправляем на логин');
      router.push('/login');
    }
  } finally {
    isLoading.value = false;
  }
};

// Функция для разблокировки пользователя
const handleUnbanUser = async (userId: number) => {
  unbanningUserId.value = userId;
  try {
    await unbanUser(userId);
    
    // Удаляем пользователя из списка после успешной разблокировки
    bannedUsers.value = bannedUsers.value.filter(user => user.id !== userId);
    console.log(`Пользователь ${userId} успешно разблокирован`);
    
  } catch (error: any) {
    console.error('Ошибка при разблокировке пользователя:', error);
    
    // Обрабатываем ошибку авторизации
    if (error.response?.status === 401) {
      console.log('Пользователь не авторизован, перенаправляем на логин');
      router.push('/login');
    }
  } finally {
    unbanningUserId.value = null;
  }
};

onMounted(() => {
  loadBannedUsers();
});
</script>

<style lang="scss" scoped>
.banned-users-container {
  padding: 16px;
  max-width: 600px;
  margin: 0 auto;
}

h2 {
  color: var(--color-text-800);
  margin-bottom: 20px;
  text-align: center;
}

.loading, .empty-state {
  text-align: center;
  padding: 40px;
  color: var(--color-text-600);
  font-size: 1.1em;
}

.users-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background-color: var(--color-background-100);
  border-radius: 8px;
  border: 1px solid var(--color-border);
}

.username {
  font-weight: 500;
  color: var(--color-text-800);
  font-size: 1.1em;
}

.unban-btn {
  background-color: var(--color-primary-400);
  color: var(--color-text-50);
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;

  &:hover:not(:disabled) {
    background-color: var(--color-primary-500);
  }

  &:disabled {
    background-color: var(--color-text-400);
    cursor: not-allowed;
    opacity: 0.7;
  }
}
</style>