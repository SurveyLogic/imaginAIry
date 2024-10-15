<template>
  <div class="w-full relative searchTopContainer" tabindex="1">
    <form
      autocomplete="off"
      class="flex w-full max:w-512 relative items-center justify-between bg-kilvish-200 rounded-full pl-18 sm:pl-32 sm:pr-8 pr-4 border border-kilvish-200 transition-all"
      :class="{
        'border border-kilvish-300 shadow-searchbox': isInputFocused,
      }"
      @focus="onSearchFocus"
      @blur="onSearchBlur"
      @submit.prevent="onSearchSubmit"
    >
      <div class="flex flex-row items-center gap-18 sm:gap-28 w-full">
        <search class="block w-30 h-30 transition-all text-black" />
        <input
          ref="searchBox"
          :value="searchTerm"
          class="appearance-none focus:outline-none text-textdark transition bg-gray-200 h-48 sm:h-56 focus:placeholder-kilvish-400 placeholder-kilvish-600 w-full"
          name="searchvalue"
          placeholder="Search or ask a question"
          @input="onSearchChange"
        />
      </div>
      <button
        type="submit"
        class="transition w-112 h-40 bg-primary hover:bg-primary-800 text-white rounded-full font-medium font-sans"
      >
        <span class="inline">Search</span>
      </button>
    </form>
    <div
      v-show="showSuggestions"
      class="search-suggestion hidden transition-all"
    >
      <SearchSuggestions
        :suggestions="suggestions"
        @forceFocus="forceFocus"
        @handleSearchChange="(e) => onSearchChange(e, true)"
        @onSearch="onSearchSubmit"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from "vue";
import Search from "../icons/Search.vue";
import SearchSuggestions from './SearchSuggestions.vue'

const props = defineProps({
  searchTerm: {
    type: String,
    default: "",
  },
  suggestions: {
    type: Object,
    default: () => ({}),
  }
});

const emit = defineEmits([
  "setSearchField",
  "onSearchSubmit",
  "onSearchChange",
]);

const isInputFocused = ref(false);
const searchBox = ref(null);

const showSuggestions = computed(() => props.searchTerm === "");

const forceFocus = () => {
  searchBox.value.focus();
  isInputFocused.value = true;
};

const onSearchFocus = () => {
  nextTick(() => {
    isInputFocused.value = true;
  });
};

const onSearchBlur = () => {
  nextTick(() => {
    isInputFocused.value = false;
  });
};

const clearInput = () => {
  emit("setSearchField", "");
  searchBox.value.focus();
};

const onSearchSubmit = () => {
  emit("onSearchSubmit", props.searchTerm);
};

const onSearchChange = (event) => {
  emit("onSearchChange", event.target.value);
};
</script>

<style scoped>
.searchTopContainer:focus-within .search-suggestion {
  display: block;
}
</style>
