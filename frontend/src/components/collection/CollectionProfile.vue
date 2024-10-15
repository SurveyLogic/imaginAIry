<template>
  <div
    class="flex flex-row"
    :class="{
      'gap-12 sm:gap-42 items-start': variant === 'large',
      'gap-16 sm:gap-25 items-center': variant === 'small',
    }"
  >
    <avatar
      class-name="text-title"
      :name="collectionName"
      :src="collectionImage"
      :size="variant === 'small' ? '60' : '136'"
      rounded="12"
      class="hidden sm:block"
    />

    <avatar
      class-name="text-title"
      :name="collectionName"
      :src="collectionImage"
      :size="variant === 'small' ? '60' : '100'"
      rounded="12"
      class="block sm:hidden"
    />

    <div
      class="flex items-start justify-start"
      :class="{
        'flex-row gap-10': variant === 'small',
        'flex-col gap-4 sm:gap-10': variant === 'large',
      }"
    >
      <a
        :href="collectionShareUrl"
        class="text-textdark font-bold leading-[1.375rem]"
        :class="{
          'text-subheader2 sm:text-heading2': variant === 'small',
          'text-subheader2 sm:text-display4 mt-8': variant === 'large',
        }"
      >
        {{ collectionName }}
      </a>

      <div
        v-if="variant === 'large'"
        class="relative flex flex-col gap-16 sm:gap-10"
      >
        <p
          class="font-medium text-caption1 sm:text-body text-kilvish-200 sm:text-textmedium desc-markdown"
          :class="{
            'text-elip text-nowrap': !isSummaryExpanded,
          }"
          v-html="getMarkdownText(collectionDescription) || ''"
        />
      </div>

      <div
        v-else
        class="flex flex-row text-center font-semibold sm:font-normal text-subheader2 sm:text-heading2 text-kilvish-300 sm:text-textdark gap-3 sm:gap-6"
      >
        <p>/</p>
        <p
          class="text-subheader2 sm:text-heading2 text-kilvish-300 sm:text-textdark sm:opacity-50"
        >
          Search
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from "marked";
import Avatar from "../atoms/Avatar.vue";

export default {
  name: "CollectionProfile",
  components: {
    Avatar,
  },
  props: {
    collectionName: {
      type: String,
      required: true,
    },
    collectionImage: {
      type: String,
      required: true,
    },
    collectionDescription: {
      type: String,
      required: true,
    },
    collectionShareUrl: {
      type: String,
      required: true,
    },
    variant: {
      type: String,
      default: 'large',
      validator: (value) => ['small', 'large'].includes(value)
    },
  },
  data() {
    return {
      isSummaryExpanded: true,
    };
  },
  methods: {
    getMarkdownText(markdown) {
      const mdown =
        markdown.length > 180 ? markdown.substring(0, 180) + "..." : markdown;
      return marked.parse(mdown);
    },
  },
};
</script>

<style scoped>
.text-elip {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@media (max-width: 640px) {
  .text-elip {
    -webkit-line-clamp: 3;
  }
}

.desc-markdown li {
  display: list-item;
  list-style: disc;
}

.desc-markdown ul {
  list-style-type: disc !important;
}
</style>
