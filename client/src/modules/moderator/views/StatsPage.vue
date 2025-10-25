<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useStatsStore } from '../store/stats';
import type { LiveStats } from '@core/api/types';
const statsStore = useStatsStore();

const stats = ref<LiveStats>()

onMounted(async () => {
    stats.value = await statsStore.getLiveStats(); 
})
</script>


<template>
    {{ stats }}
</template>


<style scoped lang="scss">

</style>