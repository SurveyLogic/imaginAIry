<template>
  <div>
    <div class="hidden md:block">
      <div
        class="flex-col justify-center bg-others-black181818 br-60 p-8"
        :class="{
          card: showGradient,
          'border border-kilvish-700 w-60': !showGradient,
        }"
      >
        <menu-button
          v-for="(elm, i) in options"
          :key="i"
          :icon="elm.icon"
          :title="elm.title"
          :button-class="i === options.length - 1 ? '' : 'mb-10'"
          @click="$emit('openChat', elm)"
        />
      </div>
    </div>
    <div
      class="flex items-center w-full md:hidden bg-white border-b border-kilvish-400 justify-between p-12"
    >
      <Button
        variant="secondary"
        classname="rounded-24 bg-kilvish-200 text-sm tt-override max-w-full overflow-hidden overflow-ellipsis whitespace-nowrap tracking-normal"
        @click="$emit('openChat', options[1])"
      >
        <img :src="options[1].icon" class="w-16 h-auto mr-8 " />
        {{ options[1].title }}
      </Button>
      <Button
        variant="primary"
        classname="rounded-24 text-sm tt-override max-w-full overflow-hidden overflow-ellipsis whitespace-nowrap tracking-normal"
        @click="$emit('openChat', options[0])"
      >
        <img :src="options[0].icon" class="w-16 h-auto mr-8" />
        {{ options[0].title }}
      </Button>
      <ai-dropdown
        :options="options"
        @openChat="(opt) => $emit('openChat', opt)"
      />
    </div>
  </div>
</template>

<script>
import MenuButton from "./MenuButton.vue";
import Button from "../atoms/Button.vue";
import AiDropdown from "./AiDropdown.vue";

export default {
  components: { MenuButton, Button, AiDropdown },
  props: {
    showGradient: {
      type: Boolean,
      default: true,
    },
    options: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.br-60 {
  border-radius: 60px;
}

.tt-override {
  text-transform: none !important;
}

@property --rotate {
  syntax: "<angle>";
  initial-value: 132deg;
  inherits: false;
}

:root {
  --card-height: 258px;
  --card-width: 60px;
}

.card {
  width: var(--card-width);
  height: var(--card-height);
  position: relative;
  justify-content: center;
  align-items: center;
  text-align: center;
  display: flex;
  color: rgb(88 199 250 / 0%);
  cursor: pointer;
}

.card:hover {
  color: rgb(88 199 250 / 100%);
  transition: color 1s;
}
.card:hover:before,
.card:hover:after {
  animation: none;
  opacity: 0;
}

.card::before {
  content: "";
  width: 104%;
  height: 102%;
  border-radius: 60px;
  background-image: linear-gradient(
    var(--rotate),
    #e2462ccc,
    #ff7635cc,
    #fcbc2ccc
  );
  position: absolute;
  z-index: -1;
  top: -1%;
  left: -2%;
  animation: spin 3s linear infinite;
  animation-delay: 0s;
}

.card::after {
  position: absolute;
  content: "";
  top: -20%;
  left: 0;
  right: 0;
  z-index: -1;
  height: 140%;
  width: 100%;
  margin: 0 auto;
  transform: scale(0.7);
  filter: blur(calc(258px / 6));
  background-image: linear-gradient(
    var(--rotate),
    #e2462ccc,
    #ff7635cc,
    #fcbc2ccc
  );
  opacity: 1;
  transition: opacity 0.5s;
  animation: spin 3s ease infinite;
  animation-delay: 0s;
}

@keyframes spin {
  0% {
    --rotate: 0deg;
  }
  100% {
    --rotate: 360deg;
  }
}
</style>
