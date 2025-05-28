import { mount } from 'cypress/vue'
import { createPinia, type Pinia } from 'pinia'
import { App } from 'vue'

declare global {
  namespace Cypress {
    interface Chainable {
      mountWithPinia(
        component: any,
        options?: Parameters<typeof mount>[1] & {
          pinia?: Pinia
          plugins?: App['_context']['plugins']
        }
      ): Chainable<any>
    }
  }
}

Cypress.Commands.add('mountWithPinia', (component, options = {}) => {
  const pinia = options.pinia || createPinia()
  
  return mount(component, {
    ...options,
    global: {
      ...options.global,
      plugins: [
        ...(options.global?.plugins || []),
        pinia
      ]
    }
  })
})