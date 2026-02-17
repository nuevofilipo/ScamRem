// src/routes/+page.js
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { fetchChannelName } from "$lib/api";

export async function load({ fetch }) {
  const auth = getAuth();

  return new Promise((resolve) => {
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        const myChannelName = await fetchChannelName();
        resolve({ 
          items: myChannelName,
          user: user 
        });
      } else {
        resolve({ 
          items: null,
          user: null 
        });
      }
    });
  });
}