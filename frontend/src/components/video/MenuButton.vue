<template>
  <popper
    hover
    arrow
    placement="left"
    :modifiers="{ offset: { offset: '0,10px' } }"
    boundaries-selector=".video-player"
    boundaries="30px"
    class="flex items-center justify-center chatMenuButton"
  >
    <template
      #content
      class="popper z-30 vdb-p-hidden sm:vdb-p-block"
      :class="!isPopperActive ? 'vdb-p-invisible' : ''"
    >
      {{ title }}
    </template>
    <div slot="reference">
      <button
        class="w-40 h-40 flex items-center justify-center rounded-full bg-black hover:bg-others-summaryHover"
        :class="buttonClass"
        @click="$emit('click')"
      >
        <img class="w-20 h-auto" :src="icon" :alt="title" />
      </button>
    </div>
  </popper>
</template>

<script setup>
import Popper from 'vue3-popper'

defineProps({
  icon: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    default: 'Open chat',
  },
  buttonClass: {
    type: String,
    default: '',
  },
  isPopperActive: {
    type: Boolean,
    default: true,
  },
})
</script>

<style>
.chatMenuButton .popper {
  border-radius: 40px;
  white-space: nowrap;
  border: none;
  padding: 4px 8px;
  box-shadow: none;
  background-color: #272727;
  color: white;
  border: 1px solid #232323;
}

.chatMenuButton .popper .popper__arrow {
  border-left-color: #272727;
}
</style>