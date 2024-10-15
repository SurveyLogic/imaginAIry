<template>
  <div
    :class="`${className}`"
    :style="{
      width: `${size}px`,
      height: `${size}px`,
      minWidth: `${size}px`,
    }"
  >
    <img
      v-if="src && src !== ''"
      :src="src"
      :class="`h-full w-full min-w-full rounded-${rounded}`"
    />
    <div
      v-else
      class="flex items-center justify-center text-white"
      :style="{ background: stringToHslColor(name) }"
      :class="`h-full w-full min-w-full rounded-${rounded}`"
    >
      {{ name.charAt(0) }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'Avatar',
  props: {
    src: {
      type: String,
      default: '',
    },
    name: {
      type: String,
      default: '',
    },
    className: {
      type: String,
      default: '',
    },
    size: {
      type: String,
      default: '60',
    },
    rounded: {
      type: String,
      default: 'full',
    },
  },
  computed: {
    backgroundImage() {
      return `url("${this.src}")`
    },
  },
  methods: {
    stringToHslColor(str, s = 80, l = 35) {
      let hash = 0
      for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash)
      }

      hash = hash % 360
      return 'hsl(' + hash + ', ' + s + '%, ' + l + '%)'
    },
  },
}
</script>
