<template>
  <div
    class="flex flex-row items-center"
    :class="{
      'gap-42': props.variant !== 'small',
      'gap-25': props.variant === 'small',
    }"
  >
    <div
      class="text-title rounded-12 animate-pulse bg-gray-300"
      :class="{
        'h-100 w-100 sm:h-182 sm:w-182': props.variant !== 'small',
        'h-42 w-42': props.variant === 'small',
      }"
    />
  </div>
</template>

<script setup>
const props = defineProps({
  variant: {
    type: String,
    default: 'large',
    validator: (value) => ['small', 'large'].includes(value)
  }
});
</script>
