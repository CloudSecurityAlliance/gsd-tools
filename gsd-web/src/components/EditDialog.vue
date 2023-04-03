<template>
  <!-- notice dialogRef here -->
  <q-dialog ref="dialogRef" @hide="onDialogHide" :persistent="unsavedChanges" full-width>
    <q-card class="q-dialog-plugin">
      <q-card-section class="bg-primary text-white text-center">
        <div class="text-h6">Edit GSD</div>
      </q-card-section>

      <q-separator />

      <q-card-section class="text-center">
        <q-toggle
          v-model="jsonEditMode"
          label="JSON Edit Mode"
          class="q-mr-md"
        />
        <q-btn
          @click="resetValues"
          :disabled="!unsavedChanges"
          color="secondary"
          label="Undo Changes"
          class="q-ml-md"
        />
      </q-card-section>

      <q-card-section style="overflow: auto; max-height: 70vh;">
        <template v-if="jsonEditMode">
          <q-input
            v-model="gsdJson"
            filled
            autogrow
            label="GSD JSON"
          />
        </template>

        <template v-else>
          <div class="q-pa-md row items-start q-col-gutter-md">
            <div class="col-12 col-md-6">
              <div class="text-h6">Summary</div>
              <q-input
                v-model="gsdSummary"
                filled
                label="Summary"
              />
              <div class="text-h6 q-mt-md">Details</div>
              <q-input
                v-model="gsdDetails"
                filled
                autogrow
                label="Details"
              />
              <div class="row items-start q-col-gutter-md">
                <div class="col-12 col-md-6">
                  <div class="text-h6 q-mt-md">Published</div>
                  <q-input
                    v-model="gsdPublished"
                    filled
                    clearable
                    placeholder="ISO8601 String"
                    label="ID Published At"
                  >
                  <template v-slot:prepend>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                        <q-date today-btn v-model="gsdPublished" mask="YYYY-MM-DDTHH:mm:ss.sssZ">
                          <div class="row items-center justify-end">
                            <q-btn v-close-popup label="Close" color="primary" flat />
                          </div>
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </template>

                  <template v-slot:append>
                    <q-icon name="access_time" class="cursor-pointer">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                        <q-time now-btn v-model="gsdPublished" mask="YYYY-MM-DDTHH:mm:ss.sssZ">
                          <div class="row items-center justify-end">
                            <q-btn v-close-popup label="Close" color="primary" flat />
                          </div>
                        </q-time>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                  </q-input>
                </div>
                <div class="col-12 col-md-6">
                  <div class="text-h6 q-mt-md">Withdrawn</div>
                  <q-input
                    v-model="gsdWithdrawn"
                    filled
                    clearable
                    placeholder="ISO8601 String"
                    label="ID Withdrawn At"
                  >
                  <template v-slot:prepend>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                        <q-date today-btn v-model="gsdWithdrawn" mask="YYYY-MM-DDTHH:mm:ss.sssZ">
                          <div class="row items-center justify-end">
                            <q-btn v-close-popup label="Close" color="primary" flat />
                          </div>
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </template>

                  <template v-slot:append>
                    <q-icon name="access_time" class="cursor-pointer">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                        <q-time now-btn v-model="gsdWithdrawn" mask="YYYY-MM-DDTHH:mm:ss.sssZ">
                          <div class="row items-center justify-end">
                            <q-btn v-close-popup label="Close" color="primary" flat />
                          </div>
                        </q-time>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                  </q-input>
                </div>
              </div>
              <div class="text-h6 q-mt-md">Severity</div>
              <hr>
              <template v-for="(severity, index) in gsdSeverity" :key="index">
                <div class="row">
                  <div class="col-auto">
                    <q-select
                      v-model="severity.type"
                      :options="severityOptions"
                      filled
                      label="Type"
                    />
                  </div>
                  <div class="col-grow">
                    <q-input
                      v-model="severity.score"
                      filled
                      class="q-ml-xs flex-grow"
                      label="Score"
                    />
                  </div>
                  <div class="col-auto">
                    <q-btn
                      color="negative"
                      icon="fa fa-trash"
                      class="q-ml-xs full-height"
                      @click="removeSeverity(index)"
                    />
                  </div>
                </div>
                <div class="row q-mt-xs">
                  <div class="col-12">
                    <q-input
                      v-model="severity.other_type"
                      filled
                      label="Other Type"
                      v-if="severity.type === 'OTHER'"
                    />
                  </div>
                </div>
                <hr>
              </template>
              <q-btn
                color="positive"
                icon="fa fa-plus"
                label="Add Severity"
                @click="addSeverity"
              />
              <div class="text-h6 q-mt-md">Credits</div>
              <hr>
              <template v-for="(credit, index) in gsdCredits" :key="index">
                <q-btn
                  color="negative"
                  icon="fa fa-trash"
                  class="full-height"
                  label="Remove Credit"
                  @click="removeCredit(index)"
                />
                <div class="row q-mt-sm">
                  <div class="col-auto">
                    <q-select
                      v-model="credit.type"
                      :options="creditOptions"
                      filled
                      label="Type"
                    />
                  </div>
                  <div class="col-grow">
                    <q-input
                      v-model="credit.name"
                      filled
                      class="q-ml-xs flex-grow"
                      label="Name"
                    />
                  </div>
                </div>
                <div class="row">
                  <div class="col-12">
                    <q-input
                      v-model="credit.other_type"
                      filled
                      class="q-mt-xs"
                      label="Other Type"
                      v-if="credit.type === 'OTHER'"
                    />
                  </div>
                </div>
                <template v-for="(contact, index) in credit.contact" :key="index">
                  <div class="row q-mt-xs">
                    <div class="col-grow">
                      <q-input
                        v-model="credit.contact[index]"
                        filled
                        label="Contact"
                      />
                    </div>
                    <div class="col-auto">
                      <q-btn
                        color="negative"
                        icon="fa fa-trash"
                        class="q-ml-xs full-height"
                        @click="removeContact(credit, index)"
                      />
                    </div>
                  </div>
                </template>
                <q-btn
                  color="positive"
                  icon="fa fa-plus"
                  label="Add Contact"
                  class="q-mt-sm"
                  @click="addContact(credit)"
                />
                <hr>
              </template>
              <q-btn
                color="positive"
                icon="fa fa-plus"
                label="Add Credits"
                @click="addCredit"
              />
            </div>
            <div class="col-12 col-md-6">
              <div class="row items-start q-col-gutter-md">
                <div class="col-12 col-md-6">
                  <div class="text-h6">Aliases</div>
                  <hr>
                  <template v-for="(alias, index) in gsdAliases" :key="index">
                    <div class="row">
                      <div class="col-grow">
                        <q-input
                          v-model="gsdAliases[index]"
                          filled
                          class="flex-grow"
                          label="ID Alias"
                        />
                      </div>
                      <div class="col-auto">
                        <q-btn
                          color="negative"
                          icon="fa fa-trash"
                          class="q-ml-xs full-height"
                          @click="removeAlias(index)"
                        />
                      </div>
                    </div>
                    <hr>
                  </template>
                  <q-btn
                    color="positive"
                    icon="fa fa-plus"
                    label="Add Alias"
                    @click="addAlias"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <div class="text-h6">Related IDs</div>
                  <hr>
                  <template v-for="(related, index) in gsdRelated" :key="index">
                    <div class="row">
                      <div class="col-grow">
                        <q-input
                          v-model="gsdRelated[index]"
                          filled
                          class="flex-grow"
                          label="Related ID"
                        />
                      </div>
                      <div class="col-auto">
                        <q-btn
                          color="negative"
                          icon="fa fa-trash"
                          class="q-ml-xs full-height"
                          @click="removeRelated(index)"
                        />
                      </div>
                    </div>
                    <hr>
                  </template>
                  <q-btn
                    color="positive"
                    icon="fa fa-plus"
                    label="Add Related ID"
                    @click="addRelated"
                  />
                </div>
              </div>
              <div class="text-h6 q-mt-md">Affected</div>
              <hr>
              <template v-for="(affected, index) in gsdAffected" :key="index">
                <q-btn
                  color="negative"
                  icon="fa fa-trash"
                  label="Remove Affected"
                  @click="removeAffected(index)"
                />
                <div class="row q-mt-sm">
                  <div class="col-auto">
                    <q-select
                      v-model="affected.package.ecosystem"
                      :options="ecosystemOptions"
                      filled
                      label="Ecosystem"
                    />
                  </div>
                  <div class="col-grow">
                    <q-input
                      v-model="affected.package.name"
                      filled
                      class="flex-grow q-mx-xs"
                      label="Package Name"
                    />
                  </div>
                  <div class="col-auto">
                    <q-input
                      v-model="affected.package.purl"
                      filled
                      label="Package URL"
                    />
                  </div>
                </div>
                <div class="row">
                  <div class="col-12">
                    <q-input
                      v-model="affected.package.other_ecosystem"
                      filled
                      class="q-mt-xs"
                      label="Other Ecosystem"
                      v-if="affected.package.ecosystem === 'OTHER'"
                    />
                  </div>
                </div>
                <hr>
                <div class="row q-mt-xs">
                  <div class="col-6">
                    <template v-for="(range, index) in affected.ranges" :key="index">
                      <q-btn
                        color="negative"
                        icon="fa fa-trash"
                        label="Remove Range"
                        @click="removeAffectedRange(affected, index)"
                      />
                      <div class="q-mt-xs">
                        <span class="text-bold">Range</span>
                      </div>
                      <div class="row">
                        <div class="col-auto">
                          <q-select
                            v-model="range.type"
                            :options="rangeOptions"
                            filled
                            label="Type"
                          />
                        </div>
                        <div class="col-grow">
                          <q-input
                            v-model="range.repo"
                            filled
                            class="q-mx-xs"
                            label="Repo"
                          />
                        </div>
                      </div>
                      <div class="q-mt-xs">
                        <span class="text-bold">Range Events</span>
                      </div>
                      <template v-for="(event, index) in range.events" :key="index">
                        <div class="row q-mt-xs">
                          <div class="col-auto">
                            <q-select
                              v-model="event.type"
                              :options="eventOptions"
                              filled
                              label="Type"
                            />
                          </div>
                          <div class="col-grow">
                            <q-input
                              v-model="event.value"
                              filled
                              class="q-mx-xs"
                              label="Value"
                            />
                          </div>
                          <div class="col-auto">
                            <q-btn
                              color="negative"
                              icon="fa fa-trash"
                              class="q-mr-xs full-height"
                              @click="removeRangeEvent(range, index)"
                            />
                          </div>
                        </div>
                      </template>
                      <q-btn
                        color="positive"
                        icon="fa fa-plus"
                        label="Add Event"
                        class="q-mt-xs"
                        @click="addRangeEvent(range)"
                      />
                      <hr>
                    </template>
                    <q-btn
                      color="positive"
                      icon="fa fa-plus"
                      label="Add Range"
                      @click="addAffectedRange(affected)"
                    />
                  </div>
                  <div class="col-6">
                    <q-select
                      label="Versions"
                      filled
                      v-model="affected.package.versions"
                      use-input
                      use-chips
                      multiple
                      hide-dropdown-icon
                      clearable
                      input-debounce="0"
                      new-value-mode="add-unique"
                      class="q-mb-xs"
                    />
                    <hr>
                    <template v-for="(severity, index) in affected.severity" :key="index">
                      <div class="row">
                        <div class="col-auto">
                          <q-select
                            v-model="severity.type"
                            :options="severityOptions"
                            filled
                            label="Type"
                          />
                        </div>
                        <div class="col-grow">
                          <q-input
                            v-model="severity.score"
                            filled
                            class="q-ml-xs flex-grow"
                            label="Score"
                          />
                        </div>
                        <div class="col-auto">
                          <q-btn
                            color="negative"
                            icon="fa fa-trash"
                            class="q-ml-xs full-height"
                            @click="removeAffectedSeverity(affected, index)"
                          />
                        </div>
                      </div>
                      <div class="row q-mt-xs">
                        <div class="col-12">
                          <q-input
                            v-model="severity.other_type"
                            filled
                            label="Other Type"
                            v-if="severity.type === 'OTHER'"
                          />
                        </div>
                      </div>
                      <hr>
                    </template>
                    <q-btn
                      color="positive"
                      icon="fa fa-plus"
                      label="Add Severity"
                      @click="addAffectedSeverity(affected)"
                    />
                  </div>
                </div>
                <hr>
              </template>
              <q-btn
                color="positive"
                icon="fa fa-plus"
                label="Add Affected"
                @click="addAffected"
              />
              <div class="text-h6 q-mt-md">References</div>
              <hr>
              <template v-for="(reference, index) in gsdReferences" :key="index">
                <div class="row">
                  <div class="col-auto">
                    <q-select
                      v-model="reference.type"
                      :options="referenceOptions"
                      filled
                      label="Type"
                    />
                  </div>
                  <div class="col-grow">
                    <q-input
                      v-model="reference.url"
                      filled
                      class="q-ml-xs flex-grow"
                      label="URL"
                    />
                  </div>
                  <div class="col-auto">
                    <q-btn
                      color="negative"
                      icon="fa fa-trash"
                      class="q-ml-xs full-height"
                      @click="removeReference(index)"
                    />
                  </div>
                </div>
                <div class="row">
                  <div class="col-12">
                    <q-input
                      v-model="reference.other_type"
                      filled
                      class="q-mt-xs"
                      label="Other Type"
                      v-if="reference.type === 'OTHER'"
                    />
                  </div>
                </div>
                <hr>
              </template>
              <q-btn
                color="positive"
                icon="fa fa-plus"
                label="Add Reference"
                @click="addReference"
              />
            </div>
          </div>
        </template>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Cancel" color="grey" v-close-popup :disabled="saving" />
        <q-btn flat label="Save Changes" color="primary" @click="saveChanges" :disabled="!unsavedChanges" :loading="saving" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { useDialogPluginComponent, useQuasar } from 'quasar'
import { computed, ref, watch, unref } from 'vue'
import { api } from 'boot/axios'

import { errorNotification } from '../misc/ErrorNotification'

import _ from 'lodash'

export default {
  name: 'EditDialog',

  props: {
    gsd_json: {
      type: String,
      required: true
    },
    identifier: {
      type: String,
      required: true
    }
  },

  emits: [
    // REQUIRED; need to specify some events that your
    // component will emit through useDialogPluginComponent()
    ...useDialogPluginComponent.emits
  ],

  setup (props, { emit }) {
    // REQUIRED; must be called inside of setup()
    const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } = useDialogPluginComponent()
    // dialogRef      - Vue ref to be applied to QDialog
    // onDialogHide   - Function to be used as handler for @hide on QDialog
    // onDialogOK     - Function to call to settle dialog with "ok" outcome
    //                    example: onDialogOK() - no payload
    //                    example: onDialogOK({ /*.../* }) - with payload
    // onDialogCancel - Function to call to settle dialog with "cancel" outcome

    const $q = useQuasar()

    const gsdJson = ref(props.gsd_json)
    const jsonEditMode = ref(false)

    let gsdJsonObject = JSON.parse(gsdJson.value)
    const gsdOriginalSummary = ref('')
    const gsdOriginalDetails = ref('')
    const gsdOriginalCredits = ref([])
    const gsdOriginalAffected = ref([])
    const gsdOriginalReferences = ref([])
    const gsdOriginalSeverity = ref([])
    const gsdOriginalAliases = ref([])
    const gsdOriginalRelated = ref([])
    const gsdOriginalPublished = ref('')
    const gsdOriginalWithdrawn = ref('')

    const saving = ref(false)

    if(gsdJsonObject.gsd !== undefined && gsdJsonObject.gsd.osvSchema !== undefined) {
      gsdOriginalSummary.value = gsdJsonObject.gsd.osvSchema.summary
      gsdOriginalDetails.value = gsdJsonObject.gsd.osvSchema.details
      if(gsdJsonObject.gsd.osvSchema.published) {
        gsdOriginalPublished.value = new Date(gsdJsonObject.gsd.osvSchema.published).toISOString()
      }
      if(gsdJsonObject.gsd.osvSchema.withdrawn) {
        gsdOriginalWithdrawn.value = new Date(gsdJsonObject.gsd.osvSchema.withdrawn).toISOString()
      }
      if(gsdJsonObject.gsd.osvSchema.credits) {
        for(const credit of gsdJsonObject.gsd.osvSchema.credits) {
          gsdOriginalCredits.value.push({ name: credit.name, contact: credit.contact, type: credit.type })
        }
      }
      if(gsdJsonObject.gsd.osvSchema.affected) {
        for(const affected of gsdJsonObject.gsd.osvSchema.affected) {
          let ranges = []
          if(affected.ranges) {
            for(const range of affected.ranges) {
              let events = []
              if(range.events) {
                for(const event of range.events) {
                  if(event.introduced) {
                    events.push({ type: 'introduced', value: event.introduced })
                  } else if(event.fixed) {
                    events.push({ type: 'fixed', value: event.fixed })
                  } else if(event.last_affected) {
                    events.push({ type: 'last_affected', value: event.last_affected })
                  } else if(event.limit) {
                    events.push({ type: 'limit', value: event.limit })
                  }
                }
              }
              ranges.push({
                type: range.type,
                repo: range.repo,
                events: events
              })
            }
          }
          gsdOriginalAffected.value.push({
            package: affected.package,
            severity: affected.severity,
            ranges: ranges,
            versions: affected.versions
          })
        }
      }
      if(gsdJsonObject.gsd.osvSchema.references) {
        for(const reference of gsdJsonObject.gsd.osvSchema.references) {
          gsdOriginalReferences.value.push({ type: reference.type, url: reference.url })
        }
      }
      if(gsdJsonObject.gsd.osvSchema.severity) {
        for(const severity of gsdJsonObject.gsd.osvSchema.severity) {
          gsdOriginalSeverity.value.push({ type: severity.type, score: severity.score })
        }
      }
      if(gsdJsonObject.gsd.osvSchema.aliases) {
        for(const alias in gsdJsonObject.gsd.osvSchema.aliases) {
          gsdOriginalAliases.value.push(alias)
        }
      }
      if(gsdJsonObject.gsd.osvSchema.related) {
        for(const related in gsdJsonObject.gsd.osvSchema.related) {
          gsdOriginalRelated.value.push(related)
        }
      }
    }

    // FIXME: Why does this only break for affected?
    gsdOriginalAffected.value = JSON.parse(JSON.stringify(gsdOriginalAffected.value))

    const gsdSummary = ref(gsdOriginalSummary.value)
    const gsdDetails = ref(gsdOriginalDetails.value)
    const gsdCredits = ref(JSON.parse(JSON.stringify(gsdOriginalCredits.value)))
    const gsdAffected = ref(JSON.parse(JSON.stringify(gsdOriginalAffected.value)))
    const gsdReferences = ref(JSON.parse(JSON.stringify(gsdOriginalReferences.value)))
    const gsdSeverity = ref(JSON.parse(JSON.stringify(gsdOriginalSeverity.value)))
    const gsdAliases = ref(JSON.parse(JSON.stringify(gsdOriginalAliases.value)))
    const gsdRelated = ref(JSON.parse(JSON.stringify(gsdOriginalRelated.value)))
    const gsdPublished = ref(gsdOriginalPublished.value)
    const gsdWithdrawn = ref(gsdOriginalWithdrawn.value)
    const referenceOptions = [
      'ADVISORY',
      'ARTICLE',
      'DISCUSSION',
      'DETECTION',
      'REPORT',
      'FIX',
      'GIT',
      'PACKAGE',
      'EVIDENCE',
      'WEB',
      'OTHER'
    ]
    const severityOptions = [
      'CVSS_V2',
      'CVSS_V3',
      'OTHER'
    ]
    const creditOptions = [
      'FINDER',
      'REPORTER',
      'ANALYST',
      'COORDINATOR',
      'REMEDIATION_DEVELOPER',
      'REMEDIATION_REVIEWER',
      'REMEDIATION_VERIFIER',
      'TOOL',
      'SPONSOR',
      'OTHER'
    ]
    const ecosystemOptions = [
      'Go',
      'npm',
      'OSS-Fuzz',
      'PyPI',
      'RubyGems',
      'crates.io',
      'Packagist',
      'Maven',
      'NuGet',
      'Linux',
      'Debian',
      'Alpine',
      'Hex',
      'Android',
      'GitHub Actions',
      'Pub',
      'ConanCenter',
      'Rocky Linux',
      'OTHER'
    ]
    const rangeOptions = [
      'SEMVER',
      'ECOSYSTEM',
      'GIT',
      'TIMESTAMP',
      'OTHER'
    ]
    const eventOptions = [
      'introduced',
      'fixed',
      'last_affected',
      'limit'
    ]

    const unsavedChanges = computed(
      () => {
        if(jsonEditMode.value) {
          return (props.gsd_json !== gsdJson.value)
        } else {
          return (
            (gsdOriginalSummary.value !== gsdSummary.value) ||
            (gsdOriginalDetails.value !== gsdDetails.value) ||
            (!(_.isEqual(gsdOriginalCredits.value, gsdCredits.value))) ||
            (!(_.isEqual(gsdOriginalAffected.value, gsdAffected.value))) ||
            (!(_.isEqual(gsdOriginalReferences.value, gsdReferences.value))) ||
            (!(_.isEqual(gsdOriginalSeverity.value, gsdSeverity.value))) ||
            (!(_.isEqual(gsdOriginalAliases.value, gsdAliases.value))) ||
            (!(_.isEqual(gsdOriginalRelated.value, gsdRelated.value))) ||
            (gsdPublished.value !== gsdOriginalPublished.value) ||
            (gsdWithdrawn.value !== gsdOriginalWithdrawn.value)
          )
        }
      }
    )

    function removeCredit(index) {
      gsdCredits.value.splice(index, 1)
    }

    function addCredit() {
      gsdCredits.value.push({ name: '', contact: [], type: 'FINDER' })
    }

    function removeAffected(index) {
      gsdAffected.value.splice(index, 1)
    }

    function addAffected() {
      gsdAffected.value.push({
        package: {
          ecosystem: 'Go',
          name: '',
          purl: ''
        },
        severity: [],
        ranges: [],
        versions: []
      })
    }

    function removeAffectedSeverity(affected, index) {
      affected.severity.splice(index, 1)
    }

    function addAffectedSeverity(affected) {
      if(affected.severity === undefined) affected.severity = [];

      affected.severity.push({ type: 'CVSS_V2', score: '' })
    }

    function removeAffectedRange(affected, index) {
      affected.ranges.splice(index, 1)
    }

    function addAffectedRange(affected) {
      if(affected.ranges === undefined) affected.ranges = [];

      affected.ranges.push({
        type: 'SEMVER',
        repo: '',
        events: []
      })
    }

    function removeRangeEvent(range, index) {
      range.events.splice(index, 1)
    }

    function addRangeEvent(range) {
      if(range.events === undefined) range.events = [];

      range.events.push({
        type: 'introduced',
        value: ''
      })
    }

    function removeAffectedVersions(affected, index) {
      affected.versions.splice(index, 1)
    }

    function addAffectedVersions(affected) {
      affected.versions.push('')
    }

    function removeReference(index) {
      gsdReferences.value.splice(index, 1)
    }

    function addReference() {
      gsdReferences.value.push({ type: 'WEB', url: '' })
    }

    function removeSeverity(index) {
      gsdSeverity.value.splice(index, 1)
    }

    function addSeverity() {
      gsdSeverity.value.push({ type: 'CVSS_V2', score: '' })
    }

    function removeAlias(index) {
      gsdAliases.value.splice(index, 1)
    }

    function addAlias() {
      gsdAliases.value.push('')
    }

    function removeRelated(index) {
      gsdRelated.value.splice(index, 1)
    }

    function addRelated() {
      gsdRelated.value.push('')
    }

    function removeContact(credit, index) {
      credit.contact.splice(index, 1)
    }

    function addContact(credit) {
      credit.contact.push('')
    }

    function resetValues() {
      gsdJson.value = props.gsd_json
      gsdSummary.value = gsdOriginalSummary.value
      gsdDetails.value = gsdOriginalDetails.value
      gsdCredits.value = JSON.parse(JSON.stringify(gsdOriginalCredits.value))
      gsdAffected.value = JSON.parse(JSON.stringify(gsdOriginalAffected.value))
      gsdReferences.value = JSON.parse(JSON.stringify(gsdOriginalReferences.value))
      gsdSeverity.value = JSON.parse(JSON.stringify(gsdOriginalSeverity.value))
      gsdAliases.value = JSON.parse(JSON.stringify(gsdOriginalAliases.value))
      gsdRelated.value = JSON.parse(JSON.stringify(gsdOriginalRelated.value))
      gsdPublished.value = gsdOriginalPublished.value
      gsdWithdrawn.value = gsdOriginalWithdrawn.value
    }

    function saveChanges() {
      saving.value = true;
      let fileContent = '';
      try {
        // Force reformatting of the JSON string, as well as check validity.
        if(jsonEditMode.value) {
          fileContent = JSON.stringify(JSON.parse(gsdJson.value), null, 2);
        } else {
          let tempGsdJson = JSON.parse(props.gsd_json);
          let tempCredits = JSON.parse(JSON.stringify(gsdCredits.value))
          let tempAffected = JSON.parse(JSON.stringify(gsdAffected.value))
          let tempReferences = JSON.parse(JSON.stringify(gsdReferences.value))
          let tempSeverity = JSON.parse(JSON.stringify(gsdSeverity.value))

          tempCredits.forEach(
            (credit) => {
              if(credit.type === 'OTHER' && credit.other_type !== undefined) {
                credit.type = credit.other_type
              }
              delete(credit.other_type)
            }
          )

          // It's turtles all the way down
          tempAffected.forEach(
            (affected) => {
              if(affected.package.ecosystem === 'OTHER' && affected.package.other_ecosystem !== undefined) {
                affected.package.ecosystem = affected.package.other_ecosystem
              }
              delete(affected.package.other_type)

              if(affected.severity) {
                affected.severity.forEach(
                  (severity) => {
                    if(severity.type === 'OTHER' && severity.other_type !== undefined) {
                      severity.type = severity.other_type
                    }
                    delete(severity.other_type)
                  }
                )
              }

              if(affected.ranges) {
                affected.ranges.forEach(
                  (range) => {
                    if(range.type === 'OTHER' && range.other_type !== undefined) {
                      range.type = range.other_type
                    }
                    delete(range.other_type)

                    if(range.events) {
                      let events = []
                      range.events.forEach(
                        (event) => {
                          if(event.type === 'introduced') {
                            events.push({ introduced: event.value })
                          } else if(event.type === 'fixed') {
                            events.push({ fixed: event.value })
                          } else if(event.type === 'last_affected') {
                            events.push({ last_affected: event.value })
                          } else if(event.type === 'limit') {
                            events.push({ limit: event.value })
                          }
                        }
                      )
                      range.events = events
                    }
                  }
                )
              }
            }
          )

          tempReferences.forEach(
            (reference) => {
              if(reference.type === 'OTHER' && reference.other_type !== undefined) {
                reference.type = reference.other_type
              }
              delete(reference.other_type)
            }
          )

          tempSeverity.forEach(
            (severity) => {
              if(severity.type === 'OTHER' && severity.other_type !== undefined) {
                severity.type = severity.other_type
              }
              delete(severity.other_type)
            }
          )

          // Set schema version to what's known/used by GSD Web
          tempGsdJson.gsd.osvSchema.schema_version = '1.4.0'
          // Set modified to current datetime, as we're modifying the entry...
          tempGsdJson.gsd.osvSchema.modified = new Date().toISOString()

          tempGsdJson.gsd.osvSchema.summary = gsdSummary.value
          tempGsdJson.gsd.osvSchema.details = gsdDetails.value
          tempGsdJson.gsd.osvSchema.credits = JSON.parse(JSON.stringify(tempCredits))
          tempGsdJson.gsd.osvSchema.affected = JSON.parse(JSON.stringify(tempAffected))
          tempGsdJson.gsd.osvSchema.references = JSON.parse(JSON.stringify(tempReferences))
          tempGsdJson.gsd.osvSchema.severity = JSON.parse(JSON.stringify(tempSeverity))
          tempGsdJson.gsd.osvSchema.aliases = JSON.parse(JSON.stringify(gsdAliases.value))
          tempGsdJson.gsd.osvSchema.related = JSON.parse(JSON.stringify(gsdRelated.value))
          if(gsdPublished.value) {
            tempGsdJson.gsd.osvSchema.published = new Date(gsdPublished.value).toISOString()
          } else if(tempGsdJson.gsd.osvSchema.published) {
            delete(tempGsdJson.gsd.osvSchema.published)
          }
          if(gsdWithdrawn.value) {
            tempGsdJson.gsd.osvSchema.withdrawn = new Date(gsdWithdrawn.value).toISOString()
          } else if(tempGsdJson.gsd.osvSchema.withdrawn) {
            delete(tempGsdJson.gsd.osvSchema.withdrawn)
          }

          fileContent = JSON.stringify(tempGsdJson, null, 2);
        }
        api.patch('/update-gsd', {
          identifier: props.identifier,
          file_content: fileContent + '\n'
        }).then(
          (response) => {
            const redirectWindow = window.open(
              response.data.redirect_url,
              '_blank'
            )
            if(!redirectWindow) {
              $q.notify({
                color: 'negative',
                position: 'top',
                message: 'Please allow pop-ups to open GitHub Pull Request',
                icon: 'report_problem'
              })
            }
            $q.notify({
              color: 'positive',
              position: 'top',
              message: 'Changes saved!',
              icon: 'published_with_changes'
            })
            saving.value = false
            onDialogOK()
          },
          (error) => {
            saving.value = false
            errorNotification(error, 'Failed to update GSD')
          }
        )
      } catch(error) {
        saving.value = false
        errorNotification(error, 'Failed to save changes')
      }
    }

    return {
      // Custom stuff
      gsdJson,
      saveChanges,
      unsavedChanges,
      jsonEditMode,
      gsdSummary,
      gsdDetails,
      gsdCredits,
      gsdAffected,
      gsdReferences,
      gsdSeverity,
      gsdAliases,
      gsdRelated,
      gsdPublished,
      gsdWithdrawn,
      creditOptions,
      ecosystemOptions,
      rangeOptions,
      eventOptions,
      referenceOptions,
      severityOptions,
      removeCredit,
      addCredit,
      removeAffected,
      addAffected,
      removeAffectedSeverity,
      addAffectedSeverity,
      removeAffectedRange,
      addAffectedRange,
      removeRangeEvent,
      addRangeEvent,
      removeAffectedVersions,
      addAffectedVersions,
      removeReference,
      addReference,
      removeSeverity,
      addSeverity,
      removeAlias,
      addAlias,
      removeRelated,
      addRelated,
      removeContact,
      addContact,
      resetValues,
      saving,

      // This is REQUIRED;
      // Need to inject these (from useDialogPluginComponent() call)
      // into the vue scope for the vue html template
      dialogRef,
      onDialogHide,

      // other methods that we used in our vue html template;
      // these are part of our example (so not required)
      onOKClick () {
        // on OK, it is REQUIRED to
        // call onDialogOK (with optional payload)
        onDialogOK()
        // or with payload: onDialogOK({ ... })
        // ...and it will also hide the dialog automatically
      },

      // we can passthrough onDialogCancel directly
      onCancelClick: onDialogCancel
    }
  }
}
</script>
