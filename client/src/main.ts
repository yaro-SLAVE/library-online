import { createApp } from "vue";
import { createPinia } from "pinia";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-icons/font/bootstrap-icons.min.css";
import "bootstrap/dist/js/bootstrap";
import "modern-normalize/modern-normalize.css";
import "@assets/style.scss";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

import App from "./App.vue";
import router from "@core/router/index";

import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import axios from "axios";
import { useAuthStore } from "@core/store/auth";

import axiosPlugin from './core/api/axios';

const app = createApp(App);

app.use(Toast);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
app.use(pinia);
app.use(router);
app.use(axiosPlugin);

app.mount("#app");
