<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide" maximized>
    <q-card class="q-dialog-plugin">
      <q-card-section class="bg-primary text-white text-center">
        <div class="text-h6">Create new GSD Identifier</div>
      </q-card-section>

      <q-separator />

      <q-card-section style="overflow: auto; max-height: 80vh;">
        <div class="row">
          <div class="col-6">
            <q-input
              filled
              label="Vendor Name"
            />
            <br>
            <q-input
              filled
              label="Product Name"
            />
            <br>
            <q-input
              filled
              label="Affect Version(s)"
            />
            <br>
            <q-input
              filled
              label="Vulnerability Type"
            />
            <br>
            <q-input
              filled
              label="Affected Component"
            />
            <q-input
              filled
              label="Attack Vector"
            />
            <br>
            <q-input
              filled
              label="Impact of Exploitation"
            />
            <br>
            <q-input
              filled
              label="Discoverer/Credit"
            />
            <br>
            <q-input
              filled
              label="References"
            />
            <q-btn
              color="positive"
              icon="fa fa-plus"
            />
            <br>
            <q-input
              filled
              autogrow
              label="Notes"
            />
          </div>
          <div class="col-6">
            <p>The description below is being generated based on your input values. Please try to make it make sense. If you edit this box manually, it will stop updating based on the other values entered. Feel free to make any manual edits needed.</p>
          </div>
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Cancel" color="grey" v-close-popup />
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
  name: 'CreateDialog',

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

    return {
      // Custom stuff

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
