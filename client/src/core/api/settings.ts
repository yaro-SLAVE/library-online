import axios from "axios";
import type { LibrarySettings } from "@api/types";

export async function getSettings(): Promise<LibrarySettings> {
  const { data } = await axios.get<LibrarySettings>("/api/settings/");
  console.log("/api/settings/", data);
  return data;
}

export async function updateSettings(settings: LibrarySettings) {
  try {
    const payload = new FormData();
    payload.append("max_books_per_order", String(settings.max_books_per_order));
    payload.append("max_books_per_reader", String(settings.max_books_per_reader));
    payload.append("max_borrow_days", String(settings.max_borrow_days));
    payload.append("new_order_wait", String(settings.new_order_wait));
    payload.append("processing_order_wait", String(settings.processing_order_wait));
    payload.append("holidays", JSON.stringify(settings.holidays ?? []));

    if (settings.logo instanceof File) {
      payload.append("logo", settings.logo);
    } else if (typeof settings.logo === "string") {
      payload.append("logo", settings.logo);
    }

    await axios.put("/api/settings/update/", payload, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  } catch (error) {
    console.error("Ошибка при обновлении настроек", error);
    throw error;
  }
}
