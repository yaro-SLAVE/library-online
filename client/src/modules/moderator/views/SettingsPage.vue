<script setup lang="ts">


import type { LibrarySettings } from "@core/api/types"
import { getSettings, updateSettings } from "@core/api/settings"
import { onBeforeMount, ref } from 'vue';
import StyledButton from "@components/StyledButton.vue";
import { Calendar, DatePicker } from 'v-calendar';
import type { DatePickerDate, DatePickerAttribute } from 'v-calendar/types/index';
import InputField from '@core/components/TextField.vue';
import dayjs from 'dayjs';

const settings = ref<LibrarySettings>({
    max_books_per_order: 0,
  max_books_per_reader: 0,
  max_borrow_days: 0,
  holidays: [],
  logo: null,
  new_order_wait: 0,
  processing_order_wait: 0,
});
const file = ref();

const calendarAttributes = ref<DatePickerAttribute[]>([
  {
    key: 'selected-dates',
    highlight: {
      color: 'green',
      fillMode: 'solid',
    },
    dates: [],
  }
]);

onBeforeMount(async() => {
    settings.value = await getSettings();
    calendarAttributes.value[0].dates = settings.value.holidays;
});

const onDayClick = (day: DatePickerDate) => {
  const dayClick = dayjs(day.date).format('YYYY-MM-DD');

  if (calendarAttributes.value[0].dates.includes(dayClick)) {
    const existingIndex = calendarAttributes.value[0].dates.indexOf(dayClick);
    calendarAttributes.value[0].dates.splice(existingIndex, 1);
  } else {
    calendarAttributes.value[0].dates.push(dayClick);
  }

  calendarAttributes.value[0].dates.sort();
};

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    file.value = target.files[0];
  }
};

async function save() {
  settings.value.holidays = calendarAttributes.value[0].dates;
  settings.value.logo = file.value;

  await updateSettings(settings.value);
}
</script>

<template>
    <div style="display: flex; flex-direction: column; margin: 15px; align-items: center; gap: 10px">
        <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
            <span>Максимальное количество книг в заказе</span>
            <InputField type="number" v-model="settings.max_books_per_order"/>
        </div>

        <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
            <span>Максимальное количество книг на руках</span>
            <InputField type="number" v-model="settings.max_books_per_reader"/>
        </div>

        <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
            <span>Максимальное количество дней на выдачу</span>
            <InputField type="number" v-model="settings.max_borrow_days"/>
        </div>

        <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
            <span>Срок ожидания нового заказа (в часах)</span>
            <InputField type="number" v-model="settings.new_order_wait"/>
        </div>

        <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
            <span>Срок задержки исполнения заказа (в часах)</span>
            <InputField type="number" v-model="settings.processing_order_wait"/>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px">
            <span>Логотип сайта</span>
            <InputField type="file" v-model="file" @change="onFileChange"/>
        </div>

        <div>
            <DatePicker
                :attributes="calendarAttributes"
                @dayclick="onDayClick"
                is-expanded
                :masks="{ input: 'YYYY-MM-DD' }"
            />
            
        </div>

        <StyledButton
          theme="primary"
          style="width: 90px"
          @click="save"
        >
          Сохранить
        </StyledButton>
    </div>
</template>

<style lang="scss" scoped>

</style>