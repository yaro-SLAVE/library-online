<template>
  <div class="container instructions-page">
    <h1>Как использовать наш сервис</h1>

    <div class="instructions">
      <SurfaceCard v-for="(step, index) in steps" v-bind:key="index" class="card">
        <h2 class="text-3xl">{{ step.title }}</h2>
        <p class="card-text">{{ step.description }}</p>
      </SurfaceCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import SurfaceCard from "@components/SurfaceCard.vue";

const steps = [
  {
    title: "Шаг 1: Регистрация",
    description:
      "Для начала необходимо зарегистрироваться на сайте. Перейдите на страницу 'Регистрация', введите свои данные и подтвердите регистрацию через email.",
  },
  {
    title: "Шаг 2: Выбор книг",
    description:
      "Вы можете выбрать книги через каталог, который находится на главной странице. Используйте фильтры поиска, чтобы ускорить процесс выбора нужных книг.",
  },
  {
    title: "Шаг 3: Добавление в корзину",
    description:
      "Нажмите на кнопку 'Добавить в корзину' рядом с книгой, чтобы добавить её в вашу корзину. Вы можете выбрать несколько книг для оформления заказа.",
  },
  {
    title: "Шаг 4: Оформление заказа",
    description:
      "Перейдите в корзину и нажмите 'Оформить заказ'. Введите ваш email для получения уведомлений о статусе заказа, и подтвердите ваш выбор.",
  },
  {
    title: "Шаг 5: Получение книг",
    description:
      "После оформления заказа, ваши книги будут готовы в течение 1-2 дней. Мы уведомим вас, как только заказ будет готов.",
  },
];
</script>

<style scoped lang="scss">
@use "@assets/styles/breakpoints.scss" as *;

.instructions-page {
  padding: 20px;
}

h1 {
  text-align: center;
}

.instructions {
  display: flex;
  flex: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}

.card {
  flex-basis: 100%;
  @include media-md {
    flex-basis: 45%;
  }
  @include media-lg {
    flex-basis: 25%;
  }
}

.card-text {
  font-size: var(--text-base);
  color: var(--color-text-700);
}
</style>
