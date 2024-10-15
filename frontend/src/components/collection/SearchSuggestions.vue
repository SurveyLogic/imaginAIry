<template>
  <div
    class="absolute flex flex-col w-full rounded-16 bg-gray-200 mt-4 p-18 border border-kilvish-300 shadow-spextlg z-30"
  >
    <div
      ref="suggestionBox"
      class="px-10 max-h-200 sm:max-h-372 overflow-y-auto"
    >
      <div>
        <div class="text-gray-450 text-caption18 uppercase">
          Popular Searches in this collection
        </div>
        <div
          v-for="(suggestion, index) in suggestions"
          :key="`suggestion-pop-${index}`"
          class="flex flex-row items-center gap-14 cursor-pointer hover:text-red text-caption1 py-8 border-b-2 border-kilvish-300 border-opacity-50"
          @click="handleSuggestionClick(suggestion.text)"
        >
          <search class="hidden md:block h-16 w-16" />
          {{ suggestion.text }}
        </div>
      </div>
    </div>
    <!-- <div class="absolute bottom-0 pb-30 py-4 w-full bg-gray-200"> -->
    <!--   <div -->
    <!--     class="absolute right-0 uppercase text-caption1 text-textdark font-semibold cursor-pointer pr-56 flex flex-row gap-12" -->
    <!--   > -->
    <!--     <div>See more</div> -->
    <!--     <img src="/icons/anchor-down.svg" /> -->
    <!--   </div> -->
    <!-- </div> -->
  </div>
</template>

<script>
import Search from '../icons/Search.vue'
export default {
  name: 'SearchSuggestions',
  components: {
    Search,
  },
  props: {
    suggestions: {
      type: Object,
      default: () => {},
    },
  },
  methods: {
    handleSuggestionClick(text) {
      this.$emit('handleSearchChange', {
        target: { value: text },
      })
      this.$emit('onSearch')
    },
  },
}
</script>
