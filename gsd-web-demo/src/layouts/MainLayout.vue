<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          <router-link to="/" class="text-white" style="text-decoration: none;">GSD Demo</router-link>
        </q-toolbar-title>

        <q-space />

        <q-btn
          label="Demo Github Repo"
          flat
          @click="openGithubRepo()"
        />

        <q-input
          v-model="searchField"
          @keyup.enter="search"
          input-class="text-right"
          class="q-ml-md"
          placeholder="GSD Search"
          dark
          dense
          standout
        >
          <template v-slot:append>
            <q-btn round dense flat icon="search" @click="search" />
          </template>
        </q-input>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default defineComponent({
  name: 'MainLayout',

  setup() {
    const $route = useRoute()
    const $router = useRouter()

    const searchField = ref($route.params.id)

    function search() {
      if (!searchField.value || typeof searchField.value !== 'string') { return }

      if (searchField.value.match(/^GSD-\d{4}-\d{4,}$/) || searchField.value.match(/^UVI-\d{4}-\d{4,}$/)) {
        $router.push({ path: `/identifier/${searchField.value}` })
      } else {
        window.open(
          `https://github.com/cloudsecurityalliance/gsd-database/search?q=${searchField.value}`,
          '_blank'
        )
      }
    }

    function openGithubRepo() {
      window.open('https://github.com/cloudsecurityalliance/gsd-demo', '_blank')
    }

    watch(
      () => $route.params.id,
      (newValue) => {
        searchField.value = newValue
      }
    )

    return {
      searchField,
      search,
      openGithubRepo,
    }
  }
})
</script>
