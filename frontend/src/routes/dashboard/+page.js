// src/routes/+page.js
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { API_BASE_URL, fetchChannelName, fetchVideos } from "$lib/api";
import {app } from "$lib/firebase";

export async function load({ fetch }) {
    const auth = getAuth(app);

    return new Promise((resolve) => {
        onAuthStateChanged(auth, async (user) => {
            if (user) {
                console.log("apparently user already signed in, page.js main page");

                // Check subscription status
                const response = await fetch(`${API_BASE_URL}/check-subscription?userId=${user.uid}`);
                const data = await response.json();

                // if (data.status !== "active") {
                //     console.log("User not subscribed, redirecting to /subscribe");
                //     goto("/dashboard/subscription");
                //     return;
                // }

                // Fetch user data only if subscribed
                await fetchVideos(null);
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
