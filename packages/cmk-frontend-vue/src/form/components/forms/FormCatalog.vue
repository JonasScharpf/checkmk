<!--
Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import type { Catalog, Topic } from '@/form/components/vue_formspec_components'
import { ref } from 'vue'
import { immediateWatch } from '@/form/components/utils/watch'
import FormCatalogDictionary from './FormCatalogDictionary.vue'
import {
  groupDictionaryValidations,
  type ValidationMessages
} from '@/form/components/utils/validation'
import HelpText from '@/components/HelpText.vue'

const props = defineProps<{
  spec: Catalog
  backendValidation: ValidationMessages
}>()

const data = defineModel<Record<string, Record<string, unknown>>>('data', { required: true })

const hiddenTopics = ref<Record<string, boolean>>({})

immediateWatch(
  () => props.spec.topics,
  () => {
    hiddenTopics.value = {}
  }
)

const elementValidation = ref<Record<string, ValidationMessages>>({})
immediateWatch(
  () => props.backendValidation,
  (newValidation: ValidationMessages) => {
    const [, _elementValidation] = groupDictionaryValidations(props.spec.topics, newValidation)
    elementValidation.value = _elementValidation
  }
)

function toggleTopic(topic: Topic) {
  hiddenTopics.value[topic.ident] = !hiddenTopics.value[topic.ident]
}

function getClass(ident: string) {
  return {
    open: !hiddenTopics.value[ident],
    closed: hiddenTopics.value[ident]
  }
}

// Disabled, will be implemented in a future version
// This function should be accessible outside of the component
// function setAllTopics(isOpen: boolean) {
//   for (const topic of props.spec.topics) {
//     hiddenTopics.value[topic.ident] = !isOpen
//   }
// }
</script>

<template>
  <!-- <input type="button" :value="props.spec.i18n.open_all" @click="setAllTopics(true)" /> -->
  <!--  <input type="button" :value="props.spec.i18n.collapse_all" @click="setAllTopics(false)" />-->
  <table
    v-for="topic in props.spec.topics"
    :key="topic.ident"
    class="nform"
    :class="getClass(topic.ident)"
  >
    <thead>
      <tr class="heading" @click="toggleTopic(topic)">
        <td colspan="2">
          <img class="vue nform treeangle" :class="getClass(topic.ident)" />
          {{ topic.dictionary.title }}
          <HelpText :help="topic.dictionary.help" />
        </td>
      </tr>
    </thead>
    <tbody :class="getClass(topic.ident)">
      <tr>
        <td colspan="2" />
      </tr>
      <FormCatalogDictionary
        v-model="data[topic.ident]!"
        :elements="topic.dictionary.elements"
        :backend-validation="elementValidation[topic.ident]!"
      />
      <tr class="bottom">
        <td colspan="2"></td>
      </tr>
    </tbody>
  </table>
</template>
