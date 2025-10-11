<template>
    <div class="app">
        <Transition name="slide">
            <div class="app-body">
                <div class="sidebar-container" v-if="isOpen">
                    <div class="sidebar">
                        <nav>
                            <RouterLink to="/">Главная</RouterLink>
                            <RouterLink to="/books">Книги</RouterLink>
                            <RouterLink to="/users">Пользователи</RouterLink>
                        </nav>
                    </div>
                </div>
                <div class="main-content">
                    <button class="toggle-btn" @click="isOpen = !isOpen" :class="{ 'is-open': isOpen }">
                        <span class="line line-top"></span>
                        <span class="line line-bottom"></span>
                    </button>
                </div>
            </div>
        </Transition>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
const isOpen = ref(false);
</script>

<style scoped>
.app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #f4f4f4;
}

.app-body {
    display: flex;
    flex: 1;
    overflow: hidden;
}

.sidebar-container {
    width: 260px;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar {
    width: 100%;
    background: aliceblue;
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 20px;
}

.sidebar nav {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.sidebar nav a {
    text-decoration: none;
    color: #333;
    padding: 8px 10px;
    border-radius: 4px;
    transition: background-color 0.3s;
}

.sidebar nav a:hover {
    background-color: #e0e0e0;
}

.main-content {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
}

.slide-enter-active,
.slide-leave-active {
    transition: transform 0.3s ease;
}


.slide-enter-from,
.slide-leave-to {
    transform: translateX(-100%);
    opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
    transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out;
}

.slide-enter-to,
.slide-leave-from {
    transform: translateX(0);
    opacity: 1;
}


.toggle-btn {
    position: relative;
    margin-right: 20px;
    width: 40px;
    height: 40px;
    background: #007bff;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: transform 0.3s ease, background-color 0.3s ease;
    padding: 0;
}

.line {
    display: block;
    width: 20px;
    height: 2px;
    background: white;
    transition: transform 0.3s ease, opacity 0.3s ease;
    position: absolute;
}

.line-top {
    transform: translateY(-3px);
}

.line-bottom {
    transform: translateY(3px);
}

.toggle-btn.is-open .line-top {
    transform: rotate(45deg);
}

.toggle-btn.is-open .line-bottom {
    transform: rotate(-45deg);
}
</style>