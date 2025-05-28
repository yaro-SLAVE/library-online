import { useAuthStore } from "@core/store/auth";
import { createTestingPinia } from '@pinia/testing'
import { setActivePinia, createPinia, storeToRefs } from 'pinia'
import axios from "axios";

describe('Counter Store', () => {
  let originalAxios: any

  beforeEach(() => {
    cy.visit('/profile')
    setActivePinia(createPinia())
    originalAxios = axios.create()
  })

  it('open orders', async () => {
    const authStore = useAuthStore()

    axios.interceptors.request.use(async (config) => {
      if (await authStore.updateTokens()) {
        config.headers.Authorization = `Bearer ${authStore.access}`
      }
      return config
    })

    const data = await authStore.login("", ""); // Здесь логин и пароль
    const { currentUserRole, access } = storeToRefs(authStore);
    currentUserRole.value = "Librarian";

    cy.visit('/')
  })
})