
import { writable, type Writable } from 'svelte/store';
import { auth } from '../firebase';
import { onAuthStateChanged, type User } from 'firebase/auth';
import { API_BASE_URL } from '$lib/api';

export const user: Writable<User | null> = writable(null);
export const subscription = writable(null);

onAuthStateChanged(auth, async (newUser: User | null) => {
  user.set(newUser);

  if (newUser) {
    const response = await fetch(`${API_BASE_URL}/check-subscription?userId=${newUser.uid}`);
    const data = await response.json();
    subscription.set(data.status === "active");
} else {
    subscription.set(null);
}
});


