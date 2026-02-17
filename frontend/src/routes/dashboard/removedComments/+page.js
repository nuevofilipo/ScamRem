import { getAuth, onAuthStateChanged } from "firebase/auth";
import { fetchRemovedComments } from "$lib/api";

export async function load() {
  const auth = getAuth();

  return new Promise((resolve) => {
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        await fetchRemovedComments(); // ✅ Updates the store, no return needed
      } else {
        console.log("User is not logged in");
      }
      resolve({}); // ✅ Return an empty object to keep SvelteKit happy
    });
  });
}
