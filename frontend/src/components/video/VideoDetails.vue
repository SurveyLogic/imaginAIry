<script setup lang="ts">
import { ref } from "vue";
import dayjs from "dayjs";
import Avatar from "../atoms/Avatar.vue";
import LinkIcon from "../icons/LinkIcon.vue";

const props = defineProps({
  videoTitle: String,
  collectionShareUrl: String,
  videoShareUrl: String,
  collectionName: String,
  collectionImage: String,
  collectionPublishDate: String,
  isLoading: Boolean,
});

const isLinkCopied = ref(false);

const copyLink = () => {
  isLinkCopied.value = true;
  console.log("copying link", props.videoShareUrl);
  navigator.clipboard.writeText(props.videoShareUrl ?? "");
  console.log("navigator.clipboard.writeText", navigator.clipboard.writeText);
  setTimeout(() => {
    isLinkCopied.value = false;
  }, 5000);
};
</script>

<template>
  <div class="xl:px-200 lg:px-142 sm:px-56 md:px-88 px-12 mt-32">
    <div v-if="!isLoading">
      <div class="flex flex-row items-start">
        <p
          class="max-w-full mb-8 font-semibold font-sans text-textdark text-heading2 sm:text-heading1 two-line-ellipses"
        >
          {{ videoTitle }}
        </p>
      </div>
      <div class="flex flex-row justify-between items-start">
        <a
          :href="collectionShareUrl ?? ''"
          class="flex items-center"
          target="_blank"
          rel="noopener noreferrer"
        >
          <avatar
            class-name="mr-16"
            :name="collectionName"
            :src="collectionImage"
          />
          <div>
            <p class="font-medium text-sm text-black">
              {{ collectionName }}
            </p>
            <p class="font-medium text-[#8C93A3] text-xs">
              {{ dayjs(collectionPublishDate).format("MMM D, YYYY") }}
            </p>
          </div>
        </a>
        <div class="relative flex flex-row sm:flex-row">
          <div
            class="absolute w-106 h-40 text-white flex flex-row items-center justify-center px-12 py-8 rounded-8 linkCopiedButton"
            :class="isLinkCopied ? 'linkCopiedButtonClicked' : ''"
          >
            Link Copied!
          </div>
          <button
            class="flex items-center px-12 py-8 font-medium text-white transition rounded-6 text-body text-dark mb-32 ml-4 sm:ml-8 sm:mb-20"
            :style="{
              zIndex: 1,
            }"
            :class="{
              'bg-green': isLinkCopied,
              'bg-primary-700 hover:bg-others-redfaded': !isLinkCopied,
            }"
            @click="copyLink()"
          >
            <LinkIcon />
            <div v-if="!isLinkCopied" class="ml-8 hidden sm:flex">
              Copy Link
            </div>
            <div v-if="isLinkCopied" class="ml-8 hidden sm:flex">Copied!</div>
          </button>
        </div>
      </div>
    </div>

    <div v-else class="px-88 mt-32">
      <div class="flex flex-col sm:flex-col">
        <div
          class="flex-grow w-full h-32 mb-8 bg-gray-300 rounded-full animate-pulse"
        />
        <div class="flex flex-row justify-between items-start">
          <div class="flex items-center mb-56">
            <div class="w-40 h-40 mr-16 bg-gray-300 rounded-8 animate-pulse" />
            <div>
              <div
                class="h-16 mb-4 bg-gray-300 rounded-full animate-pulse w-88"
              />
              <div class="w-32 h-16 bg-gray-300 rounded-full animate-pulse" />
            </div>
          </div>
          <div
            class="h-40 mb-32 bg-gray-300 rounded-8 min-w-96 animate-pulse sm:mb-20 sm:ml-40"
          />
        </div>
      </div>
    </div>
  </div>
</template>
