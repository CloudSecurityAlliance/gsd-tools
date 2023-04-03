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
          <q-btn class="q-ma-md" color="positive" label="Edit" @click="editGSD" :loading="!jsonBlob" />
        </div>
      </div>
    </div>

    <template v-if="validIdentifier">
      <div class="q-pa-md row items-start q-col-gutter-md">
        <div class="col-12 col-md-7">
          <q-card class="full-width">
            <q-card-section class="bg-primary text-white">
              <div class="text-subtitle2">Summary</div>
              <template v-if="osvData.summary">
                <div class="text-h6">{{ osvData.summary }}</div>
              </template>
              <template v-else>
                <div class="text-h6 text-italic">No summary available for {{ identifier }}</div>
              </template>
            </q-card-section>

            <q-separator />

            <q-card-section>
              <div class="text-h5">Details</div>
              <template v-if="osvData.details">
                <q-card class="q-my-md">
                  <q-card-section><div v-html="detailsHtml"></div></q-card-section>
                </q-card>
              </template>
              <template v-else>
                <p class="text-italic">No details available for {{ identifier }}</p>
              </template>
              <div class="row items-start q-col-gutter-md">
                <div class="col-12 col-md-6">
                  <div class="text-h5 q-mt-sm">Affected</div>
                  <template v-if="osvData.affected">
                    <ul>
                      <li v-for="affected, index in osvData.affected" :key="index">
                        <div class="text-bold" style="display:contents;">Ecosystem:</div> {{ affected.package.ecosystem }}
                        <br>
                        <div class="text-bold" style="display:contents;">Name:</div> {{ affected.package.name }}
                        <br>
                        <div class="text-bold" style="display:contents;">Ranges:</div>
                        <ul>
                          <li v-for="range, index in affected.ranges" :key="index">
                            <div class="text-bold" style="display:contents;">Type: </div>{{ range.type }}
                            <br>
                            <div class="text-bold" style="display:contents;">Repo: </div><a :href="range.repo" target="_blank">{{ range.repo }}</a>
                            <br>
                            <div class="text-bold" style="display:contents;">Events:</div>
                            <ul>
                              <li v-for="event, index in range.events" :key="index">
                                <div class="text-bold text-capitalize" style="display:contents;">{{ Object.keys(event)[0] }}:</div> {{ event[Object.keys(event)[0]] }}
                              </li>
                            </ul>
                          </li>
                        </ul>
                      </li>
                    </ul>
                  </template>
                  <template v-else>
                    <p class="text-italic">No affected versions available for {{ identifier }}</p>
                  </template>
                </div>
                <div class="col-12 col-md-6">
                  <div class="text-h5 q-mt-sm">Identifiers</div>
                  <q-list bordered separator>
                    <q-item clickable v-ripple :href="`https://gsd.id/${identifier}`" target="_blank">
                      <q-item-section avatar>
                        <q-icon name="gpp_maybe" />
                      </q-item-section>

                      <q-item-section>
                        {{ identifier }}
                      </q-item-section>
                    </q-item>
                    <template v-for="alias, index in osvData.aliases" :key="index">
                      <template v-if="hasAliasLink(alias)">
                        <q-item clickable v-ripple :href="aliasLink(alias)" target="_blank">
                          <q-item-section avatar>
                            <q-icon name="gpp_maybe" />
                          </q-item-section>

                          <q-item-section>
                            {{ alias }}
                          </q-item-section>
                        </q-item>
                      </template>
                      <template v-else>
                        <q-item>
                          <q-item-section avatar>
                            <q-icon name="gpp_maybe" />
                          </q-item-section>

                          <q-item-section>
                            {{ alias }}
                          </q-item-section>
                        </q-item>
                      </template>
                    </template>
                  </q-list>
                </div>
              </div>
              <div class="text-h5 q-mt-sm">References</div>
              <template v-if="osvData.references">
                <q-list bordered separator>
                  <q-item
                    clickable
                    v-ripple
                    v-for="reference, index in osvData.references"
                    :key="index"
                    :href="reference.url"
                    target="_blank"
                  >
                    <q-item-section avatar>
                      <template v-if="reference.type == 'ADVISORY'">
                        <q-icon name="gpp_maybe" />
                      </template>
                      <template v-else-if="reference.type == 'ARTICLE'">
                        <q-icon name="newspaper" />
                      </template>
                      <template v-else-if="reference.type == 'REPORT'">
                        <q-icon name="bug_report" />
                      </template>
                      <template v-else-if="reference.type == 'FIX'">
                        <q-icon name="healing" />
                      </template>
                      <template v-else-if="reference.type == 'PACKAGE'">
                        <q-icon name="code" />
                      </template>
                      <template v-else-if="reference.type == 'EVIDENCE'">
                        <q-icon name="find_in_page" />
                      </template>
                      <template v-else>
                        <q-icon name="public" />
                      </template>
                    </q-item-section>

                    <q-item-section>
                      {{ reference.url }}
                    </q-item-section>

                    <q-item-section side>
                      <span class="text-bold">{{ reference.type }}</span>
                    </q-item-section>
                  </q-item>
                </q-list>
              </template>
              <template v-else>
                <p class="text-italic">No references available for {{ identifier }}</p>
              </template>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-5">
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

// Sanitize and render markdown
import DOMPurify from 'dompurify'
import { marked } from 'marked'

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
    const osvData = computed(
      () => {
        if(jsonBlob.value && jsonBlob.value.gsd !== undefined && jsonBlob.value.gsd.osvSchema !== undefined) {
          return jsonBlob.value.gsd.osvSchema
        } else {
          return {}
        }
      }
    )
    const detailsHtml = computed(
      () => {
        if(osvData.value.details) {
          const html = DOMPurify.sanitize(marked.parse(osvData.value.details))
          return html
        } else {
          return "<!-- No Content -->"
        }
      }
    )

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

    function hasAliasLink(alias) {
      return (
        isAndroid(alias) ||
        isGo(alias) ||
        isOSV(alias) ||
        // isPYSEC(alias) || // Broken due to unpredictable canonical URL
        isRUSTSEC(alias) ||
        isGSD(alias) ||
        isGHSA(alias) ||
        // isLBSEC(alias) || // Abandoned?
        // isDSA(alias) || // Broken due to unpredictable canonical URL
        isCVE(alias)
      )
    }

    function aliasLink(alias) {
      if(isAndroid(alias)) {
        return `https://storage.googleapis.com/android-osv/${alias}.json`
      } else if(isGo(alias)) {
        return `https://pkg.go.dev/vuln/${alias}`
      } else if(isOSV(alias)) {
        return `https://osv.dev/vulnerability/${alias}`
      } else if(isRUSTSEC(alias)) {
        return `https://rustsec.org/advisories/${alias}`
      } else if(isGSD(alias)) {
        return `https://gsd.id/${alias}`
      } else if(isGHSA(alias)) {
        return `https://github.com/advisories/${alias}`
      } else if(isCVE(alias)) {
        return `https://www.cve.org/CVERecord?id=${alias}`
      } else {
        return '#'
      }
    }

    function isValidIdentifier(value) {
      return isGSD(value)
    }

    function isAndroid(value) {
      return (value.match(/^(ASB-A|A)-\d{4,}$/))
    }

    function isGo(value) {
      return (value.match(/^GO-\d{4}-\d{4,}$/))
    }

    function isOSV(value) {
      return (value.match(/^OSV-\d{4}-\d{1,}$/))
    }

    // function isPYSEC(value) {
    //   return (value.match(/^PYSEC-\d{4}-\d{1,}$/))
    // }

    function isRUSTSEC(value) {
      return (value.match(/^RUSTSEC-\d{4}-\d{4,}$/))
    }

    function isGSD(value) {
      return (value.match(/^GSD-\d{4}-\d{4,}$/))
    }

    function isGHSA(value) {
      return (value.match(/^GHSA-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}$/))
    }

    // function isLBSEC(value) {
    //   return (value.match(/^lbsa-\d{8}$/))
    // }

    // function isDSA(value) {
    //   return (value.match(/^DSA-\d{4}$/))
    // }

    function isCVE(value) {
      return (value.match(/^CVE-\d{4}-\d{4,}$/))
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

    const username = ref('')
    username.value = $q.cookies.get('GSD-USERNAME')

    const loginURL = `https://github.com/login/oauth/authorize?client_id=${process.env.GSD_GITHUB_KEY}&scope=public_repo`

    function editGSD() {
      // TODO: Raise error or something?
      if (!isValidIdentifier(identifier.value)) { return }

      // const repo = 'https://github.com/cloudsecurityalliance/gsd-database'
      // const branch = 'main'

      // const year = identifier.value.split('-')[1]
      // const thousands = `${identifier.value.split('-')[2].slice(0, -3)}xxx`

      // const editUrl = `${repo}/edit/${branch}/${year}/${thousands}/${identifier.value}.json`

      if(username.value) {
        $q.dialog({
          component: EditDialog,

          componentProps: {
            gsd_json: JSON.stringify(jsonBlob.value, null, 2),
            identifier: identifier.value
          }
        })
      } else {
        $q.dialog({
          title: 'Currently Signed Out',
          message: 'To edit a GSD entry, you must first login to GitHub.',
          ok: {
            label: 'Sign in with GitHub',
            icon: 'fab fa-github',
            color: 'black'
          },
          cancel: true
        }).onOk(
          () => {
            const currentPath = encodeURI($route.path)
            $q.cookies.set('returnTo', currentPath)
            window.open(loginURL, '_self')
          }
        )
      }
    }

    return {
      jsonBlob,
      identifier,
      validIdentifier,
      osvData,
      detailsHtml,
      hasAliasLink,
      aliasLink,
      //
      editGSD,
      //
      isSimpleString,
      isSimpleNumber,
      isArrayOfStrings,
      isGHSA,
    }
  }
})
</script>

<style lang="sass">
</style>
