import { auth } from "./firebase.js";
import { getIdToken } from "firebase/auth";
import axios from "axios";
import { cachedRemovedComments, cachedVideos, nextPageTokenStoreVideo } from "./stores/dataStore.js";
import { channelNameStore } from "./stores/dataStore.js";
import { get } from "svelte/store"; // Required to manually extract store value
import { showNotification } from "./stores/notificationStore.js";

// export const API_BASE_URL = "https://scamrem-backend-production.up.railway.app";
export const API_BASE_URL = "http://127.0.0.1:5000";



export async function fetchChannelName() {
    const user = auth.currentUser;
    let idToken = null;

    if (user) {
      idToken = await getIdToken(user);
    } else {
      throw new Error("User not logged in yet, refresh page and try again");
    }

    const response = await axios.get(`${API_BASE_URL}/fetch_channel_name`, {
      headers: {
        Authorization: `Bearer ${idToken}`,
        "Content-Type": "application/json",
      },
    });

    let data = response.data;
    return data["channel_name"];
  }



 export async function fetchRemovedComments() {
    const user = auth.currentUser;
    let idToken = null;

    if (user) {
      idToken = await getIdToken(user);
    } else {
      console.log("User not logged in");
      return;
    }

    const response = await axios.get(`${API_BASE_URL}/fetch_removed_comments`, {
      headers: {
        Authorization: `Bearer ${idToken}`,
        "Content-Type": "application/json",
      },
    });

    let removedCommentData = response.data;
    cachedRemovedComments.set(removedCommentData);
  }



 export async function fetchVideos(token) {
    let channelName = await fetchChannelName();

    const user = auth.currentUser;
    let idToken = null;

    if (user) {
      idToken = await getIdToken(user);
    }

    const response = await axios.get(`${API_BASE_URL}/get_youtube_videos`, {
      params: {
        channel_name: channelName,
        next_page_token: token,
      },
      headers: {
        Authorization: `Bearer ${idToken}`,
        "Content-Type": "application/json",
      },
    });

    let videoData = [];
    if (token === null) {
      videoData = [];
    } else {
      videoData = get(cachedVideos);
    }

    videoData = [...videoData, ...response.data.videos]; // append new videos to the existing ones
    nextPageTokenStoreVideo.set(response.data.next_page_token);
    cachedVideos.set(videoData);
  }

  export async function setChannelName(channelname) {
    const user = auth.currentUser;
    let idToken = null;

    if (user) {
      idToken = await getIdToken(user);
    }

    try {
      const response = await axios.post(
        `${API_BASE_URL}/set_channel_name`,
        {
          channel_name: channelname,
        },
        {
          headers: {
            Authorization: `Bearer ${idToken}`,
            "Content-Type": "application/json",
          },
        }
      );

      channelNameStore.set(channelname);
      showNotification("Channel name updated successfully", "success");
    } catch (error) {
      console.error("Axios Error:", error.response ? error.response.data : error.message);
      showNotification("error updating channel name, please contact developer team", "error");
    }
  }