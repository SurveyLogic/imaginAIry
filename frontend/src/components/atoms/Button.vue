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
import { buttonTheme as theme } from "./theme";

export default {
  props: {
    type: {
      type: String,
      default: "button",
    },
    onClick: {
      type: Function,
      default: () => null,
    },
    size: {
      type: String,
      default: "normal",
    },
    variant: {
      type: String,
      default: "primary",
    },
    classname: {
      type: String,
      default: "",
    },
  },
  computed: {
    computedClass() {
      return [
        "base",
        theme.base,
        theme.sizes[this.size],
        theme.variants[this.variant],
        this.classname,
      ];
    },
  },
  methods: {
    emitClick() {
      this.onClick();
      this.$emit("click");
    },
  },
};
</script>

<style scoped lang="css">
.base {
  letter-spacing: 0.04em;
}
</style>
