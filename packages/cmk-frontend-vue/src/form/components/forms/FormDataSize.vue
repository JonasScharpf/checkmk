<!--
Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import type { DataSize } from '@/form/components/vue_formspec_components'
import { useValidation, type ValidationMessages } from '@/form/components/utils/validation'
import FormValidation from '@/form/components/FormValidation.vue'
import { useId } from '@/form/utils'
import DropDown from '@/components/DropDown.vue'
import { computed } from 'vue'

const props = defineProps<{
  spec: DataSize
  backendValidation: ValidationMessages
}>()

const data = defineModel<[string, string]>('data', { required: true })
const [validation, value] = useValidation<[string, string]>(
  data,
  props.spec.validators,
  () => props.backendValidation
)

const componentId = useId()

const magnitudeOptions = computed(() => {
  return props.spec.displayed_magnitudes.map((element: string) => {
    return {
      ident: element,
      name: element
    }
  })
})
</script>

<template>
  <label v-if="props.spec.label" :for="componentId">{{ props.spec.label }}</label>
  <input
    :id="componentId"
    v-model="value[0]"
    :placeholder="spec.input_hint || ''"
    class="number"
    type="text"
  />
  <DropDown v-model:selected-option="value[1]" :options="magnitudeOptions" />
  <FormValidation :validation="validation"></FormValidation>
</template>
