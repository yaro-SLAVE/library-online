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
  library_card: string;
  fullname: string;
}

// Получить список забаненных пользователей
export async function fetchBannedUsers(): Promise<BannedUser[]> {
  try {
    const response = await axios.get("/api/profile/banned/");
    console.log('Полный ответ:', response.data);
    
    // Теперь бэкенд возвращает данные в нужном формате
    const bannedUsers = response.data.banned_users.map((user: any) => ({
      id: user.id,
      library_card: user.library_card,
      fullname: user.fullname
    }));
    
    console.log('Преобразованные данные:', bannedUsers);
    return bannedUsers;
  } catch (error) {
    console.error("Ошибка при получении черного списка пользователей:", error);
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

// Тип для кандидата на блокировку
export interface BanCandidate {
  user_id: number;
  library_card: string;
  fullname: string;
  total_orders_count: number;
  cancelled_orders_count: number;
}

// Получить кандидатов на блокировку
export async function fetchBanCandidates(startDate: string, endDate: string): Promise<BanCandidate[]> {
  try {
    const response = await axios.get(`/api/profile/banned/candidates_for_ban/${startDate}/${endDate}/`);
    console.log('Получены кандидаты на блокировку:', response.data);
    return response.data.ban_candidates;
  } catch (error) {
    console.error("Ошибка при получении кандидатов на блокировку:", error);
    throw error;
  }
}

// Заблокировать пользователя
export async function banUser(userId: number): Promise<void> {
  try {
    await axios.put(`/api/profile/banned/ban/${userId}/`);
  } catch (error) {
    console.error("Ошибка при блокировке пользователя:", error);
    throw error;
  }
}