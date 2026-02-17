import { writable } from "svelte/store";

export const notifications = writable([]); // Store multiple notifications

export function showNotification(message, type = "info", duration = 5000) {
  const id = Date.now(); // Unique ID for each notification

  notifications.update((n) => [...n, { id, message, type }]); // Add new notification

  setTimeout(() => {
    notifications.update((n) => n.filter((notif) => notif.id !== id)); // Remove after duration
  }, duration);
}
