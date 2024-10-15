<template>
  <div class="flex flex-col h-full video-card px-30 sm:p-0">
    <div
      class="flex flex-col sm:flex-row sm:block mb-24"
      :class="{ 'flex-grow': borderB }"
    >
      <div
        class="w-auto min-w-96 sm:w-full sm:min-w-auto sm:mr-24 sm:min-w-0 sm:mb-16"
      >
        <div class="relative rounded-12 bg-white overflow-hidden vid-pb">
          <div
            class="thumbnail rounded-12 absolute top-0 left-0 right-0 bottom-0 bg-cover bg-no-repeat bg-center shadow-1 h-106"
            :style="{
              backgroundImage: item.thumbnail_url ? `url('${item.thumbnail_url}')` : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            }"
          >
            <div v-if="!item.thumbnail_url" class="absolute inset-0 flex items-center justify-center text-white text-xl font-bold">
              {{ item.name ? item.name.split(' ').slice(0, 3).join(' ') + '...' : 'Video...' }}
            </div>
          </div>
          <div
            class="flex absolute top-1/2 left-1/2 h-48 w-48 lg:h-56 lg:w-56 rounded-full items-center justify-center transform -translate-x-1/2 -translate-y-1/2 center-button transparent-button"
          >
            <PlayIcon class="h-20 w-20" />
          </div>
        </div>
      </div>
      <div class="text-black flex flex-col justify-center fade-on-hover">
        <p class="text-subheader font-medium mb-8 text-elip whitespace-normal">
          {{ item.name}}
        </p>
        <div class="flex items-center">
          <div class="flex items-center mr-16">
            <TimeIcon class="w-16 mr-2" />
            <p class="text-caption1 font-medium text-textlight">
              {{ secondsToHHMMSS(item.length || 0) }}
            </p>
          </div>
          <div class="flex items-center text-textlight">
            <comment-line class-name="w-16 mr-2" />
            <p class="text-caption1 font-medium text-textlight">
              {{ item.comments ? Object.keys(item.comments).length : 0 }}
            </p>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="borderB"
      class="border-b border-outline-xlight lg:mb-16"
      :class="`${index % 2 === 0 ? 'sm:-mr-32' : 'sm:mr-0'} ${
        index % 3 !== 2 ? 'md:-mr-32' : 'md:mr-0'
      } ${index % 4 !== 3 ? 'lg:-mr-32' : 'lg:mr-0'} ${borderClass}`"
    />
  </div>
</template>

<script>
import CommentLine from '../icons/CommentLine.vue'
import PlayIcon from '../icons/play.vue'
import TimeIcon from '../icons/time.vue'

export default {
  name: 'VideoCard',
  components: {
    CommentLine,
    PlayIcon,
    TimeIcon,
  },
  props: {
    item: {
      type: Object,
      default: () => {},
    },
    index: {
      type: Number,
      default: 0,
    },
    borderB: {
      type: Boolean,
      default: false,
    },
    borderClass: {
      type: String,
      default: '',
    },
  },
  methods: {
    secondsToHHMMSS(val) {
      if (!val) return '00:00:00'
      let time = ''
      time = new Date(val * 1000).toISOString().substring(11, 19)
      if (time.substring(0, 2) === '00') {
        return time.substring(3, time.length)
      }
      return time
    },
  },
}
</script>

<style scoped>
.transparent-button {
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.24);
  backdrop-filter: blur(16px);
  color: #fff;
  opacity: 0;
}

.vid-pb {
  padding-bottom: 75%;
}

.text-elip {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.center-button,
.fade-on-hover {
  transition: all 0.3s ease-in-out;
}
.thumbnail {
  transition: transform 0.5s linear;
  transform-origin: center;
  transform: scale(1.001);
}
@media (max-width: 640px) {
  .thumbnail {
    height: 106px;
  }
  .vid-pb {
    padding-bottom: 40%;
  }
}

@media (any-hover: hover) {
  .video-card:hover .center-button {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.05);
    background: rgba(0, 0, 0, 0.32);
    transform-origin: center;
  }
  .video-card:hover .fade-on-hover {
    opacity: 0.6;
  }
  .video-card:hover .thumbnail {
    transform: scale(1.05);
  }
}
</style>
