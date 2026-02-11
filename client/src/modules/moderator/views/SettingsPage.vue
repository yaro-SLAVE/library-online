<script setup lang="ts">
import { computed, onBeforeMount, ref } from "vue";
import dayjs from "dayjs";
import StyledButton from "@components/StyledButton.vue";
import { DatePicker } from "v-calendar";
import InputField from "@core/components/TextField.vue";
import { getSettings, updateSettings } from "@core/api/settings";
import type { LibrarySettings } from "@core/api/types";

const settings = ref<LibrarySettings>({
  max_books_per_order: 0,
  max_books_per_reader: 0,
  max_borrow_days: 0,
  holidays: [],
  logo: null,
  new_order_wait: 0,
  processing_order_wait: 0,
});
const file = ref<File | null>(null);

type DayClickPayload = {
  date: Date | string;
};

type CalendarAttribute = {
  key: string;
  highlight: {
    color: string;
    fillMode: string;
  };
  dates: string[];
};

const calendarAttributes = ref<CalendarAttribute[]>([
  {
    key: "selected-dates",
    highlight: {
      color: "green",
      fillMode: "solid",
    },
    dates: [],
  },
]);

const toNumber = (value: string): number => {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
};

const maxBooksPerOrder = computed({
  get: () => String(settings.value.max_books_per_order),
  set: (value: string) => {
    settings.value.max_books_per_order = toNumber(value);
  },
});

const maxBooksPerReader = computed({
  get: () => String(settings.value.max_books_per_reader),
  set: (value: string) => {
    settings.value.max_books_per_reader = toNumber(value);
  },
});

const maxBorrowDays = computed({
  get: () => String(settings.value.max_borrow_days),
  set: (value: string) => {
    settings.value.max_borrow_days = toNumber(value);
  },
});

const newOrderWait = computed({
  get: () => String(settings.value.new_order_wait),
  set: (value: string) => {
    settings.value.new_order_wait = toNumber(value);
  },
});

const processingOrderWait = computed({
  get: () => String(settings.value.processing_order_wait),
  set: (value: string) => {
    settings.value.processing_order_wait = toNumber(value);
  },
});

onBeforeMount(async () => {
  settings.value = await getSettings();
  calendarAttributes.value[0].dates = [...(settings.value.holidays ?? [])];
});

const onDayClick = (day: DayClickPayload) => {
  const dayClick = dayjs(day.date).format("YYYY-MM-DD");
  const selectedDates = calendarAttributes.value[0].dates;

  if (selectedDates.includes(dayClick)) {
    const existingIndex = selectedDates.indexOf(dayClick);
    selectedDates.splice(existingIndex, 1);
  } else {
    selectedDates.push(dayClick);
  }

  selectedDates.sort();
};

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    file.value = target.files[0];
  }
};

async function save() {
  settings.value.holidays = [...calendarAttributes.value[0].dates];
  settings.value.logo = file.value;

  await updateSettings(settings.value);
}
</script>

<template>
  <div style="display: flex; flex-direction: column; margin: 15px; align-items: center; gap: 10px">
    <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
      <span>Максимальное количество книг в заказе</span>
      <InputField type="number" v-model="maxBooksPerOrder" />
    </div>

    <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
      <span>Максимальное количество книг на руках</span>
      <InputField type="number" v-model="maxBooksPerReader" />
    </div>

    <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
      <span>Максимальное количество дней на выдачу</span>
      <InputField type="number" v-model="maxBorrowDays" />
    </div>

    <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
      <span>Срок ожидания нового заказа (в часах)</span>
      <InputField type="number" v-model="newOrderWait" />
    </div>

    <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 8px">
      <span>Срок задержки исполнения заказа (в часах)</span>
      <InputField type="number" v-model="processingOrderWait" />
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px">
      <span>Логотип сайта</span>
      <InputField type="file" @change="onFileChange" />
    </div>

    <div>
      <DatePicker
        :attributes="calendarAttributes"
        @dayclick="onDayClick"
        is-expanded
        :masks="{ input: 'YYYY-MM-DD' }"
      />
    </div>

    <StyledButton theme="primary" style="width: 90px" @click="save"> Сохранить </StyledButton>
  </div>
</template>

<style lang="scss" scoped></style>
