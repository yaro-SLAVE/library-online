import axios from "axios"
import type { LibrarySettings } from "@api/types"

export async function getSettings(): Promise<LibrarySettings> {
    const { data } = await axios.get("/api/settings/");
    console.log("/api/settings/", data);
    return data;
}