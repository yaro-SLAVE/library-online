<script setup lang="ts">
import type { LibrarySettings } from "@core/api/types"
import { getSettings } from "@core/api/settings"
import { onBeforeMount, ref } from 'vue';
import StyledButton from "@components/StyledButton.vue";
// import { Calendar, DatePicker } from 'v-calendar';
// import type { DatePickerDate, DatePickerAttribute } from 'v-calendar/types/index';

interface SelectedDate {
  id: string;
  date: Date;
}

const settings = ref<LibrarySettings>();

// const selectedDates = ref<SelectedDate[]>([]);

// For v-calendar attributes
// const calendarAttributes = ref<DatePickerAttribute[]>([
//   {
//     key: 'selected-dates',
//     highlight: {
//       color: 'green',
//       fillMode: 'solid',
//     },
//     dates: selectedDates.value.map(d => d.date),
//   },
//   {
//     key: 'today',
//     highlight: {
//       color: 'blue',
//       fillMode: 'light',
//     },
//     dates: new Date(),
//   }
// ]);

onBeforeMount(async() => {
    settings.value = await getSettings();
});

// const onDayClick = (day: DatePickerDate) => {
//   const dateId = day.id;
//   const existingIndex = selectedDates.value.findIndex(d => d.id === dateId);

//   if (existingIndex > -1) {
//     // Remove if already selected
//     selectedDates.value.splice(existingIndex, 1);
//   } else {
//     // Add new date
//     selectedDates.value.push({
//       id: day.id,
//       date: new Date(day.date)
//     });
//   }

//   // Update calendar attributes reactively
//   calendarAttributes.value[0].dates = selectedDates.value.map(d => d.date);
  
//   // Sort dates chronologically
//   selectedDates.value.sort((a, b) => a.date.getTime() - b.date.getTime());
// }

// const removeDate = (dateToRemove: SelectedDate) => {
//   selectedDates.value = selectedDates.value.filter(
//     date => date.id !== dateToRemove.id
//   );
//   calendarAttributes.value[0].dates = selectedDates.value.map(d => d.date);
// }

// const clearAllDates = () => {
//   selectedDates.value = [];
//   calendarAttributes.value[0].dates = [];
// }

// const formatDate = (date: Date) => {
//   return date.toLocaleDateString('ru-RU', {
//     day: 'numeric',
//     month: 'long',
//     year: 'numeric'
//   });
// }

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

        <!-- <div>
            <DatePicker
                :attributes="calendarAttributes"
                @dayclick="onDayClick"
                is-expanded
                :masks="{ input: 'DD.MM.YYYY' }"
            />
            
        </div> -->

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