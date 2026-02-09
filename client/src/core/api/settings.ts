import axios from "axios";
import type { LibrarySettings } from "@api/types";

export async function getSettings(): Promise<LibrarySettings> {
    const { data } = await axios.get("/api/settings/");
    console.log("/api/settings/", data);
    return data;
}

export async function updateSettings(settings: LibrarySettings) {
    try {
        await axios.put(`/api/settings/update/`, {
        max_books_per_order: settings.max_books_per_order,
        max_books_per_reader: settings.max_books_per_reader,
        logo: settings.logo,
        holidays: settings.holidays,
        new_order_wait: settings.new_order_wait,
        processing_order_wait: settings.processing_order_wait
        }, {
            headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
    } catch (error) {
        console.error("Ошибка при настроек", error);
        throw error;
    }
}