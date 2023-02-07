<template>
  <q-page>
    <div class="row items-start justify-evenly q-col-gutter-md q-ma-md">
      <div class="col-grow">
        <div class="text-h3 text-center">
          <template v-if="validIdentifier">
            {{ identifier }}
          </template>

          <template v-else>
            Invalid Identifier
          </template>
        </div>

        <div class="text-center" v-if="validIdentifier">
          <q-btn class="q-ma-md" color="positive" label="Edit" @click="editGSD" />
        </div>
      </div>
    </div>

    <template v-if="validIdentifier">
      <div class="row items-start justify-evenly q-col-gutter-md q-ma-md">
        <div class="col-grow">
          <div class="q-pa-md" style="max-width: 100vw;">
            <q-expansion-item
              class="shadow-1 overflow-hidden"
              style="border-radius: 30px;"
              icon="terminal"
              label="Raw JSON Data"
              header-class="bg-primary text-white"
              expand-icon-class="text-white"
            >
              <q-card style="background: #2d2d2d;">
                <q-card-section style="overflow: auto; max-height: 80vh;">
                  <a
                    :href="`https://api.gsd.id/${identifier}`"
                    target="_blank"
                    v-if="jsonBlob"
                    style="color: white;"
                  >
                    https://api.gsd.id/{{ identifier }}
                  </a>
                  <pre class="line-numbers" v-if="jsonBlob"><code class="language-json">{{ jsonBlob }}</code></pre>
                  <p v-else style="color: white;">Invalid identifier.</p>
                </q-card-section>
              </q-card>
            </q-expansion-item>
          </div>
        </div>
      </div>

      <div class="row items-start justify-evenly q-col-gutter-md q-ma-md" v-for="namespace in namespaces" :key="namespace">
        <div class="col-grow">
          <q-card bordered>
            <q-card-section class="bg-primary text-white">
              <div class="text-h5">{{ namespace }}</div>
            </q-card-section>

            <q-separator />

            <q-card-section horizontal class="bg-primary">
              <q-markup-table
                class="bg-primary full-width text-center"
                dark
                flat
                separator="cell"
              >
                <thead class="bg-dark">
                  <tr>
                    <th>Key</th>
                    <th>Value</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="key in Object.keys(jsonBlob[namespace])" :key="key">
                    <td class="text-right">{{ key }}</td>
                    <td class="text-left">
                      <div style="max-height: 50vh; max-width: 80vw; overflow: auto;">
                        <template v-if="isSimpleString(jsonBlob[namespace][key])">
                          <div style="white-space: pre-line;">
                            {{ jsonBlob[namespace][key] }}
                          </div>
                        </template>

                        <template v-else-if="isArrayOfStrings(jsonBlob[namespace][key])">
                          <ul>
                            <li v-for="element in jsonBlob[namespace][key]" :key="element">
                              {{ element }}
                            </li>
                          </ul>
                        </template>

                        <template v-else-if="isSimpleNumber(jsonBlob[namespace][key])">
                          {{ jsonBlob[namespace][key] }}
                        </template>

                        <!-- Fallback to rendering JSON -->
                        <template v-else>
                          <pre class="line-numbers" v-if="jsonBlob"><code class="language-json">{{ jsonBlob[namespace][key] }}</code></pre>
                        </template>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </q-markup-table>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </template>

    <template v-else>
      <div class="text-center q-pa-md flex flex-center">
        <div>
          <div class="text-h2" style="opacity:.4">
            Oops. Nothing here...
          </div>

          <q-btn
            class="q-mt-xl"
            color="purple"
            to="/"
            label="Go Home"
            no-caps
          />
        </div>
      </div>
    </template>
  </q-page>
</template>

<script>
import { defineComponent, ref, watch, nextTick, computed } from 'vue'
import { useQuasar } from 'quasar'
import { useRoute, useRouter } from 'vue-router'
import { gsdApi } from 'boot/axios'

// Syntax highlighting for JSON
import Prism from 'prismjs'

// Edit Dialog Component
import EditDialog from 'components/EditDialog.vue'

export default defineComponent({
  name: 'PageIdentifier',

  setup() {
    const $q = useQuasar()
    const $route = useRoute()
    const $router = useRouter()

    const identifier = ref(decodeURIComponent($route.params.id))
    const jsonBlob = ref('')
    const validIdentifier = ref(true)

    function updateJsonBlob() {
      validIdentifier.value = true

      if (!identifier.value || typeof identifier.value !== 'string') {
        validIdentifier.value = false
        return
      }

      if (isValidIdentifier(identifier.value)) {
        gsdApi.get(`/${identifier.value}`).then(
          (response) => {
            if (response.status === 200 && response.data !== '404: Not Found') {
              jsonBlob.value = response.data
            } else {
              validIdentifier.value = false
            }
          },
          (error) => {
            validIdentifier.value = false
          }
        )
      } else {
        validIdentifier.value = false
      }
    }

    // Update on mount
    updateJsonBlob()

    const namespaces = computed(
      () => {
        if (typeof jsonBlob.value != 'object') { return [] }

        if(jsonBlob.value.hasOwnProperty('namespaces') && typeof jsonBlob.value.namespaces == 'object') {
          const rootLevelKeys = Object.keys(jsonBlob.value).filter(
            (key) => {
              return key !== 'namespaces'
            }
          )
          const namespacedKeys = Object.keys(jsonBlob.value.namespaces)

          return [...rootLevelKeys, ...namespacedKeys]
        } else {
          return Object.keys(jsonBlob.value)
        }
      }
    )

    watch(
      () => jsonBlob.value,
      (newValue) => {
        nextTick().then(
          () => { Prism.highlightAll() }
        )
      }
    )

    watch(
      () => $route.params.id,
      (newValue) => {
        identifier.value = decodeURIComponent(newValue)
        jsonBlob.value = ''

        // update any time the identifier changes
        updateJsonBlob()
      }
    )

    function isValidIdentifier(value) {
      return (value.match(/^GSD-\d{4}-\d{4,}$/))
    }

    function isSimpleString(value) {
      return typeof value === 'string'
    }

    function isSimpleNumber(value) {
      return typeof value === 'number'
    }

    function isArrayOfStrings(value) {
      return (
        Array.isArray(value) &&
        value.every(
          (el) => typeof el === 'string'
        )
      )
    }

    function editGSD() {
      // TODO: Raise error or something?
      if (!isValidIdentifier(identifier.value)) { return }

      // const repo = 'https://github.com/cloudsecurityalliance/gsd-database'
      // const branch = 'main'

      // const year = identifier.value.split('-')[1]
      // const thousands = `${identifier.value.split('-')[2].slice(0, -3)}xxx`

      // const editUrl = `${repo}/edit/${branch}/${year}/${thousands}/${identifier.value}.json`

      $q.dialog({
        component: EditDialog,

        componentProps: {
          gsd_json: JSON.stringify(jsonBlob.value, null, 2),
          identifier: identifier.value
        }
      })
    }

    return {
      jsonBlob,
      identifier,
      namespaces,
      validIdentifier,
      //
      editGSD,
      //
      isSimpleString,
      isSimpleNumber,
      isArrayOfStrings,
    }
  }
})
</script>

<style lang="sass">
// FIXME: I hate css, and it hates me. Please make this look prettier.
.fancy-table
  width: 100%
  border: 1px solid
  border-collapse: collapse
  td
    border: 1px solid #ddd
    padding: 8px
  tr:nth-child(even)
    background-color: #f2f2f2
  td:hover // I'm very tempted to remove this hover effect, tbh.
    background-color: #ddd
  td:nth-child(odd)
    background-color: #0b2f5e
    color: white
    font-weight: bold
</style>
