<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          <router-link to="/home" class="text-white" style="text-decoration: none;">GSD Web</router-link>
        </q-toolbar-title>

        <q-space />

        <q-btn
          label="Contribute"
          flat
          @click="openGithubRepo()"
        />

        <q-btn
          label="Create GSD"
          flat
          @click="openCreateDialog"
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

        <q-no-ssr>
          <template v-if="username">
            <q-btn
              dense
              flat
              no-wrap
              class="q-ml-md"
            >
              <q-avatar rounded size="32px">
                <q-icon :name="githubAvatar" style="border-radius: 50%;" />
              </q-avatar>
              <q-icon name="arrow_drop_down" size="24px" />

              <q-menu auto-close>
                <q-list>
                  <q-item>
                    <q-item-section class="text-center">
                      <div>Logged in as:</div>
                      <div>
                        {{ username }}
                      </div>
                    </q-item-section>
                  </q-item>
                  <q-separator />
                  <q-item clickable @click="logout">
                    <q-item-section>Logout</q-item-section>
                    <q-item-section avatar>
                      <q-icon name="fas fa-sign-out-alt" />
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </template>

          <template v-else>
            <q-btn
              label="Sign in with GitHub"
              class="q-ml-md"
              icon="fab fa-github"
              color="black"
              @click="login"
            />
          </template>
        </q-no-ssr>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios'

// Create Dialog Component
import CreateDialog from 'components/CreateDialog.vue'

export default defineComponent({
  name: 'MainLayout',

  setup() {
    const $q = useQuasar()
    const $route = useRoute()
    const $router = useRouter()

    const searchField = ref($route.params.id)

    function search() {
      if (!searchField.value || typeof searchField.value !== 'string') { return }

      if (searchField.value.match(/^GSD-\d{4}-\d{4,}$/) || searchField.value.match(/^UVI-\d{4}-\d{4,}$/)) {
        $router.push({ path: `/${searchField.value}` })
      } else {
        window.open(
          `https://github.com/cloudsecurityalliance/gsd-database/search?q=${searchField.value}`,
          '_blank'
        )
      }
    }

    function openGithubRepo() {
      window.open('https://github.com/cloudsecurityalliance/gsd-tools/tree/main/gsd-web#gsd-web', '_blank')
    }

    function openCreateDialog() {
      $q.dialog({
        component: CreateDialog
      })
    }

    watch(
      () => $route.params.id,
      (newValue) => {
        searchField.value = newValue
      }
    )

    const loginURL = `https://github.com/login/oauth/authorize?client_id=${process.env.GSD_GITHUB_KEY}&scope=public_repo`

    function login() {
      // TODO: Auto redirect back to current page after login
      // const currentURL = encodeURI(window.location.origin + $route.path)
      window.open(loginURL, '_self')
    }

    function logout() {
      api.delete('/logout', {}).then(
        () => {
          window.location.reload()
        }
      )
    }

    const username = ref('')
    username.value = $q.cookies.get('GSD-USERNAME')

    const githubAvatar = computed(
      // FIXME: This is a fast way to get injection attacks, don't do it
      () => { return `img:https://github.com/${username.value}.png?size=128` }
    )

    return {
      searchField,
      search,
      openGithubRepo,
      openCreateDialog,
      login,
      loginURL,
      username,
      githubAvatar,
      logout,
    }
  }
})
</script>
