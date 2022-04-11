<template>
  <q-page class="flex flex-center">
    <img
      alt="Cloud Security Alliance logo"
      src="~assets/csa-logo.svg"
      style="width: 75vw; max-width: 600px;"
    >
    <p>{{ csrfToken }}</p>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'PageIndex',

  setup() {
    const $q = useQuasar()
    const csrfToken = ref('No CSRF Token')

    csrfToken.value = $q.cookies.get('XSRF-TOKEN')

    return { csrfToken }
  }
})
</script>
