<template>
  <!-- notice dialogRef here -->
  <q-dialog ref="dialogRef" @hide="onDialogHide" :persistent="unsavedChanges">
    <q-card class="q-dialog-plugin">
      <q-card-section class="bg-primary text-white text-center">
        <div class="text-h6">Edit GSD</div>
      </q-card-section>

      <q-separator />

      <q-card-section style="overflow: auto; max-height: 80vh;">
        <q-input
          v-model="gsdJson"
          filled
          autogrow
          label="GSD JSON"
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Cancel" color="grey" v-close-popup />
        <q-btn flat label="Save Changes" color="primary" @click="saveChanges" :disabled="!unsavedChanges" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { useDialogPluginComponent, useQuasar } from 'quasar'
import { computed, ref, watch } from 'vue'
import { api } from 'boot/axios'

import { errorNotification } from '../misc/ErrorNotification'

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

    const unsavedChanges = computed(
      () => {
        return (props.gsd_json !== gsdJson.value)
      }
    )

    // console.log(unsavedChanges.value)

    // watch(
    //   () => gsdJson.value,
    //   (newValue) => {
    //     console.log(unsavedChanges.value)
    //   }
    // )

    function saveChanges() {
      let fileContent = '';
      try {
        // Force reformatting of the JSON string, as well as check validity.
        fileContent = JSON.stringify(JSON.parse(gsdJson.value), null, 2);
        api.patch('/update-gsd', {
          identifier: props.identifier,
          file_content: fileContent
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
                message: 'Failed to open issue in a new tab',
                icon: 'report_problem'
              })
            }
            $q.notify({
              color: 'positive',
              position: 'top',
              message: 'Changes saved!',
              icon: 'published_with_changes'
            })
            onCancelClick()
          },
          (error) => {
            errorNotification(error, 'Failed to update GSD')
          }
        )
      } catch(error) {
        errorNotification(error, 'Failed to save changes')
      }
    }

    return {
      // Custom stuff
      gsdJson,
      saveChanges,
      unsavedChanges,

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

