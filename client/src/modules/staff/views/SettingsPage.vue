<script setup lang="ts">
import type { LibrarySettings } from "@core/api/types"
import { getSettings } from "@core/api/settings"
import { onBeforeMount, ref } from 'vue';
import StyledButton from "@components/StyledButton.vue";

const settings = ref<LibrarySettings>();

onBeforeMount(async() => {
    settings.value = await getSettings();
});

</script>

<template>
    <div style="display: flex; flex-direction: column; margin: 15px; align-items: center; gap: 10px">
        <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
            <span>Максимальное количество книг в заказе</span>
            <input type="number" v-model="settings.max_books_per_order"/>
        </div>

        <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
            <span>Максимальное количество книг на руках</span>
            <input type="number" v-model="settings.max_books_per_reader"/>
        </div>

        <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
            <span>Максимальное количество дней на выдачу</span>
            <input type="number" v-model="settings.max_borrow_days"/>
        </div>

        <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
            <span>Срок ожидания нового заказа (в часах)</span>
            <input type="number" v-model="settings.new_order_wait"/>
        </div>

        <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
            <span>Срок задержки исполнения заказа (в часах)</span>
            <input type="number" v-model="settings.processing_order_wait"/>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px">
            <span>Логотип сайта</span>
            <input type="file"/>
        </div>

        <StyledButton
          theme="primary"
          style="width: 90px"
        >
          Сохранить
        </StyledButton>
    </div>
</template>

<style lang="scss" scoped>

</style>