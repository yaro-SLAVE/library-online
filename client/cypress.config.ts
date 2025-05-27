import { defineConfig } from 'cypress'
import webpackConfig from './vite.config'

export default defineConfig({
  component: {
    devServer: {
      framework: 'vue',
      bundler: 'webpack',
      webpackConfig
    }
  },
  e2e: {
    baseUrl: 'http://localhost:5173'
  }
})
