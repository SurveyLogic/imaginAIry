<template>
  <button
    :type="type"
    :class="computedClass"
    :disabled="variant === 'disabled'"
    @click="emitClick()"
  >
    <slot />
  </button>
</template>

<script>
import { iconbuttonTheme as theme } from './theme'

export default {
  props: {
    type: {
      type: String,
      default: 'button',
    },
    onClick: {
      type: Function,
      default: () => null,
    },
    size: {
      type: String,
      default: 'normal',
    },
    variant: {
      type: String,
      default: 'normal',
    },
    classname: {
      type: String,
      default: '',
    },
  },
  computed: {
    computedClass() {
      return [
        theme.base,
        theme.sizes[this.size],
        theme.variants[this.variant],
        'iconbutton',
        this.classname,
      ]
    },
  },
  methods: {
    emitClick() {
      this.onClick()
      this.$emit('click')
    },
  },
}
</script>

<style>
</style>
