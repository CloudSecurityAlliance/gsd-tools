import { boot } from 'quasar/wrappers'
import axios from 'axios'

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
let api, gsdApi;

if (process.env.DEV) {
  api = axios.create({ baseURL: 'https://localhost:8080' })
  gsdApi = axios.create({ baseURL: 'http://localhost:8787' })
} else {
  api = axios.create({ baseURL: 'https://data.gsd.id' });
  gsdApi = axios.create({ baseURL: 'https://api.gsd.id' });
}

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API

  app.config.globalProperties.$gsdApi = gsdApi
})

export { api, gsdApi }
