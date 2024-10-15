<template>
  <div class="flex flex-col h-full">
    <div class="flex sm:block mb-30" :class="{ 'flex-grow': borderB }">
      <div
        class="w-96 min-w-96 sm:w-full sm:min-w-auto mr-24 sm:min-w-0 sm:mb-16"
      >
        <div
          class="relative rounded-12 bg-gray-400 animate-pulse custom-duration"
          style="padding-bottom: 75%"
        />
      </div>
      <div class="flex flex-col justify-center">
        <div class="animate-pulse custom-duration h-20 bg-gray-400 mb-8 rounded-full" />
        <div class="flex items-center">
          <div class="animate-pulse custom-duration w-48 h-20 bg-gray-400 rounded-full mr-12" />
          <div class="animate-pulse custom-duration w-48 h-20 bg-gray-400 rounded-full" />
        </div>
      </div>
    </div>
    <div
      v-if="borderB"
      class="border-b border-outline-xlight lg:mb-16"
      :class="`${index % 2 === 0 ? 'sm:-mr-32' : 'sm:mr-0'} ${
        index % 3 !== 2 ? 'md:-mr-32' : 'md:mr-0'
      } ${index % 4 !== 3 ? 'lg:-mr-32' : 'lg:mr-0'}`"
    />
  </div>
</template>

<script>
export default {
  name: 'VideoCardLoading',
  props: {
    index: {
      type: Number,
      default: 0,
    },
    borderB: {
      type: Boolean,
      default: false,
    },
  },
}
</script>
