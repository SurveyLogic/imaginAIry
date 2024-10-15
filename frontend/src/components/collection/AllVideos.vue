<template>
  <div class="grid grid-cols-12 gap-24 sm:gap-32 mb-24 sm:mb-32">
    <router-link
      v-for="(item, index) in videoResults"
      :key="`post-${item.id}`"
      :to="`/${item.collection_id}/video/${item.id}`"
      class="col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-3"
    >
      <video-card
        :item="item"
        :border-b="true"
        :index="index"
        border-class="sm:hidden"
      />
    </router-link>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import VideoCard from "../video/VideoCard.vue";

const props = defineProps({
  videoResults: {
    type: Array,
    default: () => [],
  },
  chatToken: {
    type: String,
    default: "",
  },
});

onMounted(() => {
  console.log("VideoResults", props.videoResults);
});
</script>