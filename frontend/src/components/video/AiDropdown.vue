<template>
  <div>
    <div @click="toggleDropdown">
      <icon-button
        classname="dropdown-toggle rounded-full m-auto"
        size="normal"
      >
        <img src="/icons/ai_sparkle.png" alt="More options" />
      </icon-button>
    </div>
    <div
      v-if="show"
      class="bg-white border border-outline-xlight rounded-12 p-16 shadow-4 z-40 bottom-72 right-30 absolute w-256 text-black"
    >
      <h3 class="text-kilvish text-sm mb-20 font-semibold">
        Suggested Follow-up Actions
      </h3>
      <button
        v-for="(opt, i) in filteredOptions"
        :key="i"
        class="w-full p-2 flex items-center max-w-full overflow-hidden overflow-ellipsis whitespace-nowrap"
        :class="{
          'mb-20': i !== filteredOptions.length - 1,
        }"
        @click="$emit('openChat', opt)"
      >
        <img :src="opt.icon" class="w-20 h-auto mr-12" />
        {{ opt.title }}
      </button>
    </div>
  </div>
</template>

<script>
import IconButton from "../atoms/IconButton.vue";

export default {
  components: {
    IconButton,
  },
  props: {
    options: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      show: false,
    };
  },
  computed: {
    filteredOptions() {
      return this.options.slice(2);
    },
  },
  methods: {
    toggleDropdown(event) {
      console.log("toggleDropdown");
      this.show = !this.show;
      if (this.show) {
        // Add event listener when dropdown is opened
        document.addEventListener("click", this.handleOutsideClick);
      } else {
        // Remove event listener when dropdown is closed
        document.removeEventListener("click", this.handleOutsideClick);
      }
    },
    closeDropdown() {
      this.show = false;
      document.removeEventListener("click", this.handleOutsideClick);
    },
    handleOutsideClick(event) {
      // Check if the click is outside the dropdown
      if (!this.$el.contains(event.target)) {
        this.closeDropdown();
      }
    },
  },
  beforeDestroy() {
    // Clean up the event listener when component is destroyed
    document.removeEventListener("click", this.handleOutsideClick);
  },
};
</script>
