<script setup>
import { computed, ref, onMounted, nextTick } from "vue";
import { useRoute } from "vue-router";

import axios from "axios";
import { v4 as uuidv4 } from "uuid";

import { ChatInterface } from "@videodb/chat-vue";
import "@videodb/chat-vue/dist/style.css";

import AllVideosLoader from "../components/collection/AllVideosLoader.vue";
import AllVideos from "../components/collection/AllVideos.vue";
import CollectionProfile from "../components/collection/CollectionProfile.vue";
import CollectionProfileLoading from "../components/collection/CollectionProfileLoading.vue";
import SearchField from "../components/collection/SearchField.vue";

import searchSuggestionsData from "../data/collection/searchSuggestions.json";

const BACKEND_URL = import.meta.env.VITE_APP_BACKEND_URL;

const route = useRoute();
const collectionId = route.params.collectionId || "default";

const appRootUrl = ref("");
const chatInterfaceRef = ref(null);

const collectionData = ref(null);
const collectionVideos = ref(null);
const videos = computed(() => {
  if (collectionVideos.value === null) {
    return [];
  }
  return collectionVideos.value;
});
const currentSessionId = ref(null);

onMounted(() => {
  // fetchData();
});
onMounted(() => {
  appRootUrl.value = window.location.origin;
});

// const fetchData = () => {
//   try {
//     axios
//       .get(`${BACKEND_URL}/videodb/collection/${collectionId}`)
//       .then((collectionResponse) => {
//         console.log("this is collection response", collectionResponse);
//         collectionData.value = collectionResponse.data;
//       });

//     axios
//       .get(`${BACKEND_URL}/videodb/collection/${collectionId}/video`)
//       .then((collectionVideosResponse) => {
//         console.log(
//           "this is collection videos response",
//           collectionVideosResponse
//         );
//         collectionVideos.value = collectionVideosResponse.data;
//       });
//   } catch (error) {
//     console.error("Error fetching collection data:", error);
//   }
// };

const searchContent = ref("");
const searchSuggestions = ref(searchSuggestionsData);

const handleSearch = (query) => {
  openChat();
};

const openChat = () => {
  const uid = uuidv4();
  currentSessionId.value = uid;

  nextTick(() => {
    if (chatInterfaceRef.value) {
      chatInterfaceRef.value.addMessage([
        {
          type: "text",
          text: searchContent.value,
        },
      ]);
    }
  });
};

const handleBackButton = () => {
  searchContent.value = "";
  currentSessionId.value = null;
};
</script>

<template>
  <main>
    <chat-interface
      ref="chatInterfaceRef"
      assistant-image="https://avatars.githubusercontent.com/u/153916971"
      :search-suggestions="searchSuggestions"
      :share-url="`${appRootUrl}/chat/${currentSessionId}`"
      :chat-hook-config="{
        socketUrl: `${BACKEND_URL}/chat`,
        httpUrl: `${BACKEND_URL}`,
        debug: true,
      }"
      collection-id="default"
      :video-id="null"
      @backBtnClick="handleBackButton"
    />
  </main>
</template>

<style>
:root {
  --popper-theme-background-color: #333333;
  --popper-theme-background-color-hover: #333333;
  --popper-theme-text-color: #ffffff;
  --popper-theme-border-width: 0px;
  --popper-theme-border-style: solid;
  --popper-theme-border-radius: 8px;
  --popper-theme-padding: 4px 8px;
  --popper-theme-box-shadow: 0px 6px 6px rgba(0, 0, 0, 0.08);
}

.template {
  height: 100vh;
  width: 100vw;
}

main {
  overflow: scroll;
  height: 100%;
}
html {
  overflow: hidden;
}
</style>
