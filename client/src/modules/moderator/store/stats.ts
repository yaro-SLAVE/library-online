import { defineStore } from "pinia";
import type { LiveStats } from "@core/api/types";
import { liveStats } from "@core/api/stats";
export const useStatsStore = defineStore("stats", () => {
 
    async function getLiveStats() : Promise<LiveStats> {
        return await liveStats();
    }
 
    return {
        getLiveStats
    };
});
