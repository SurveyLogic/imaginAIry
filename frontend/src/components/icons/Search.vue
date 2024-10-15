<template>
  <svg
    :class="className"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      fill-rule="evenodd"
      clip-rule="evenodd"
      d="M13.7929 13.7929C14.1834 13.4024 14.8166 13.4024 15.2071 13.7929L20.7071 19.2929C21.0976 19.6834 21.0976 20.3166 20.7071 20.7071C20.3166 21.0976 19.6834 21.0976 19.2929 20.7071L13.7929 15.2071C13.4024 14.8166 13.4024 14.1834 13.7929 13.7929Z"
      fill="white"
    />
    <path
      fill-rule="evenodd"
      clip-rule="evenodd"
      d="M10 5C7.23858 5 5 7.23858 5 10C5 12.7614 7.23858 15 10 15C12.7614 15 15 12.7614 15 10C15 7.23858 12.7614 5 10 5ZM3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10Z"
      fill="white"
    />
  </svg>
</template>

<script>
export default {
  name: 'Search',
  props: {
    className: {
      type: String,
      default: '',
    },
  },
}
</script>

<style scoped>
svg path {
  fill: currentColor;
}
</style>
