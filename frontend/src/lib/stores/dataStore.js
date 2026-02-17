import { writable } from 'svelte/store';

export const cachedRemovedComments = writable(null);
export const cachedComments = writable(null);
export const cachedVideos = writable(null);
export const channelNameStore = writable(""); // Store for channel name
export const nextPageTokenStoreComment = writable(null);
export const nextPageTokenStoreVideo = writable(null);