<template>
  <div class="grid grid-cols-12 gap-24 sm:gap-32">
    <div
      v-for="(item, index) in [1, 2, 3, 4]"
      :key="`post-loading-${index}`"
      class="col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-3"
    >
      <video-card-loader :index="index" />
    </div>
  </div>
</template>

<script>

import VideoCardLoader from '../video/VideoCardLoader.vue'
export default {
  name: 'AllVideoLoader',
  components:{
    VideoCardLoader,
  }
}
</script>
