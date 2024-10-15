import { createRouter, createWebHistory } from 'vue-router';
import Collection from '../views/Collection.vue';
import Video from '../views/Video.vue';

const routes = [
  {
    path: '/:collectionId',
    name: 'Collection',
    component: Collection,
  },
  {
    path: '/:collectionId/video/:videoId',
    name: 'Video',
    component: Video,
  },
  {
    path: '/default',
    name: 'Default',
    component: Collection,
  },
  {
    path: '/',
    name: 'Default-2',
    component: Collection,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
