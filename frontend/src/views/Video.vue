<script setup>
import { useRoute } from "vue-router";
import { ref, onMounted, reactive, watch } from "vue";

import { v4 as uuidv4 } from "uuid";
import axios from "axios";
import debounce from "lodash.debounce";

import {
  VideoDBPlayer,
  BigCenterButton,
  SearchInsideMedia,
} from "@videodb/player-vue";
import "@videodb/player-vue/dist/style.css";

import { ChatInterface } from "@videodb/chat-vue";
import "@videodb/chat-vue/dist/style.css";

import VideoMenu from "../components/video/VideoMenu.vue";
import VideoDetails from "../components/video/VideoDetails.vue";

import searchResultsData from "../data/video/searchResults.json";
import searchSuggestionsData from "../data/video/searchSuggestions.json";

import chatSuggestionData from "../data/video/chatSuggestions.json";

const BACKEND_URL = import.meta.env.VITE_APP_BACKEND_URL;

const route = useRoute();

// Extract the video ID from the route parameters
const collectionId = route.params.collectionId;
const videoId = route.params.videoId;

const appRootUrl = ref("");
const videoData = ref(null);
const collectionData = ref(null);

// New refs for video menu and gradient
const showVideoMenu = ref(false);
const showGradient = ref(false);

// Fetch video and collection data
const fetchData = () => {
  try {
    axios
      .get(`${BACKEND_URL}/videodb/collection/${collectionId}/video/${videoId}`)
      .then((videoResponse) => {
        console.log("videoResponse", videoResponse.data);
        videoData.value = videoResponse.data;
      });

    axios
      .get(`${BACKEND_URL}/videodb/collection/${collectionId}`)
      .then((collectionResponse) => {
        console.log("collectionResponse", collectionResponse.data);
        collectionData.value = collectionResponse.data;
      });
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

onMounted(fetchData);
onMounted(() => {
  appRootUrl.value = window.location.origin;
});

// Watch for changes in videoData and collectionData
watch([videoData, collectionData], ([newVideoData, newCollectionData]) => {
  if (newVideoData && newCollectionData) {
    showVideoMenu.value = true;
    showGradient.value = true;
    setTimeout(() => {
      showGradient.value = false;
    }, 5000);
  }
});

const videoPlayer = ref(null);

// Related to Players
const isFullScreen = ref(false);

// Related to Chat
const currentSessionId = ref(null);
const chatQuery = ref("");

// Related to search
const searchContent = ref("");
const searchSuggestions = ref(searchSuggestionsData);
const showSearchResults = ref(false);

const searchResultsLoading = ref(true);
const searchResults = reactive({
  hits: [],
});

// Methods
const openChat = (options) => {
  console.log(options);
  if (options?.query) {
    chatQuery.value = options.query;
  }
  const uid = uuidv4();
  currentSessionId.value = uid;
  if (videoPlayer.value) {
    videoPlayer.value.pause();
  }
};

const handleBackButton = () => {
  searchContent.value = "";
  currentSessionId.value = null;
};

const handleSearchChange = (query) => {
  searchContent.value = query;
  searchResultsLoading.value = true;
  debounce(function (query) {
    const newValue = query.trim();
    if (!newValue || newValue.length < 2) {
      searchResults.hits = [];
    } else {
      searchResults.hits = searchResultsData.hits;
    }
    searchResultsLoading.value = false;
  }, 500)(query);
};

const handleSearchSubmit = (query) => {
  searchContent.value = query;
};

const handleFullScreenChange = (value) => {
  isFullScreen.value = value;
  if (value) {
    document.documentElement.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
};
</script>

<template>
  <div>
    <div class="relative">
      <!-- Video Player -->
      <div
        class="w-full bg-black flex justify-center items-center"
        v-if="videoData"
      >
        <div
          :class="isFullScreen ? 'w-screen h-screen' : 'videoPlayerContainer'"
        >
          <VideoDBPlayer
            ref="videoPlayer"
            :class="isFullScreen ? 'w-screen h-screen' : ''"
            :stream-url="videoData?.stream_url"
            :default-overlay="false"
            @fullScreenChange="handleFullScreenChange"
          >
            <template v-slot:overlay>
              <BigCenterButton class="absolute top-1/2 left-1/2" />
              <SearchInsideMedia
                :search-content="searchContent"
                :search-suggestions="searchSuggestions"
                :search-results="searchResults"
                :search-results-loading="searchResultsLoading"
                :show-search-results="showSearchResults"
                @toggle-results="showSearchResults = $event"
                @search-change="handleSearchChange"
                @search-submit="handleSearchSubmit"
              />
            </template>
          </VideoDBPlayer>
        </div>
      </div>

      <!-- Video Player Loading -->
      <div v-else class="w-full bg-[#EEEFF2] flex justify-center items-center">
        <div class="videoPlayerContainer">
          <div class="w-full h-full animate-pulse aspect-video"></div>
        </div>
      </div>

      <!-- Video Menu -->
      <video-menu
        v-if="showVideoMenu"
        class="flex w-full md:w-auto md:block md:absolute md:top-1/2 md:-translate-y-1/2 md:right-16"
        :show-gradient="showGradient"
        :options="[
          {
            icon: 'https://avatars.githubusercontent.com/u/153916972',
            title: 'Open chat',
            click: openChat,
            query: null,
          },
          {
            icon: 'https://avatars.githubusercontent.com/u/153916972',
            title: 'Generate thumbnail',
            click: openChat,
            query: 'Generate a thumbnail for this video',
          },
          {
            icon: 'https://avatars.githubusercontent.com/u/153916972',
            title: 'Search',
            click: openChat,
            query: 'Search in this video',
          },
          {
            icon: 'https://avatars.githubusercontent.com/u/153916972',
            title: 'Summarize',
            click: openChat,
            query: 'Summarize this video',
          },
        ]"
        @openChat="openChat"
      />
    </div>
    <!-- Video Details -->
    <!-- <div class="xl:px-200 lg:px-142 sm:px-56 md:px-88 px-12"> -->
    <VideoDetails
      :is-loading="!videoData || !collectionData"
      :video-title="videoData?.name"
      :collection-share-url="`${appRootUrl}/${collectionData?.id}`"
      :video-share-url="`${appRootUrl}/${collectionData?.id}/video/${videoData?.id}`"
      :collection-name="collectionData?.name"
      :collection-image="collectionData?.image"
      :collection-publish-date="collectionData?.pub_date"
    />

    <chat-interface
      v-if="currentSessionId"
      assistant-image="https://avatars.githubusercontent.com/u/153916972"
      :search-suggestions="chatSuggestionData"
      :share-url="`${appRootUrl}/chat/${currentSessionId}`"
      :chat-hook-config="{
        sessionId: currentSessionId,
        collectionId: collectionData?.id,
        videoId: videoData?.id,
        url: `${BACKEND_URL}/chat`,
        debug: true,
      }"
      @backBtnClick="handleBackButton"
    />
  </div>
</template>

<style>
.videoPlayerContainer {
  width: 100%;
  height: 55vh;
  position: relative;
  display: flex;
  justify-content: center;
}

@media (min-width: 640px) {
  .videoPlayerContainer {
    width: 90%;
    height: auto;
    margin: auto;
    position: relative;
  }
}

@media (min-width: 1024px) {
  .videoPlayerContainer {
    width: 80%;
    height: auto;
  }
}

@media (min-width: 1280px) {
  .videoPlayerContainer {
    width: 70%;
    height: auto;
  }
}
</style>