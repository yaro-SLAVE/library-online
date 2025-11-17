import axios from "axios";
import type { ProfileInfo } from "./types";

export async function profileInfo(): Promise<ProfileInfo> {
  try {
    const { data } = await axios.get("/api/profile/self-info/");
    console.log("/api/profile/self-info/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении информации о профиле", error);
    throw error;
  }
}

export interface BannedUser {
  id: number;
  username: string;
}

// Получить список забаненных пользователей
export async function fetchBannedUsers(): Promise<BannedUser[]> {
  try {
    const response = await axios.get("/api/profile/banned/");
    console.log('Полный ответ:', response.data);
    
    // Преобразуем данные из формата бэкенда в наш формат
    const bannedUsers = response.data.banned_users.map((user: any) => ({
      id: user.id,
      username: user.user__username // преобразуем user__username в username
    }));
    
    console.log('Преобразованные данные:', bannedUsers);
    return bannedUsers;
  } catch (error) {
    console.error("Ошибка при получении списка забаненных пользователей:", error);
    throw error;
  }
}

// Разблокировать пользователя
export async function unbanUser(userId: number): Promise<void> {
  try {
    await axios.delete(`/api/profile/banned/unban/${userId}/`);
  } catch (error) {
    console.error("Ошибка при разблокировке пользователя:", error);
    throw error;
  }
}