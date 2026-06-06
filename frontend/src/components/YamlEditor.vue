<template>
  <div class="yaml-editor" ref="editorRef" />
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import { EditorState } from '@codemirror/state'
import { EditorView, keymap, drawSelection, highlightActiveLine, EditorView as EditorViewType } from '@codemirror/view'
import { defaultKeymap, history, historyKeymap } from '@codemirror/commands'
import { highlightWhitespace } from '@codemirror/view'
import { yaml } from '@codemirror/lang-yaml'
import { oneDark } from '@codemirror/theme-one-dark'

interface Props {
  modelValue: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const editorRef = ref<HTMLElement | null>(null)
let view: EditorViewType | null = null

const updateListener = EditorView.updateListener.of((update) => {
  if (update.docChanged) {
    const newValue = update.state.doc.toString()
    emit('update:modelValue', newValue)
  }
})

onMounted(() => {
  const startState = EditorState.create({
    doc: props.modelValue,
    extensions: [
      history(),
      defaultKeymap,
      historyKeymap,
      keymap.of([
        { key: 'Mod-s', preventDefault: true, run: () => { return false } }
      ]),
      drawSelection(),
      highlightActiveLine(),
      highlightWhitespace(),
      updateListener,
      oneDark,
      yaml()
    ]
  })

  if (editorRef.value) {
    view = new EditorView({
      state: startState,
      parent: editorRef.value
    })
  }
})

watch(() => props.modelValue, (newValue) => {
  if (view && view.state.doc.toString() !== newValue) {
    view.dispatch({
      changes: { from: 0, to: view.state.doc.length, insert: newValue }
    })
  }
})

onBeforeUnmount(() => {
  if (view) {
    view.destroy()
    view = null
  }
})

defineExpose({
  getValue: () => view?.state.doc.toString() || ''
})
</script>

<style scoped>
.yaml-editor {
  width: 100%;
  height: 600px;
  border: 1px solid #363645;
  border-radius: 8px;
  overflow: hidden;
}
</style>
