<script>
  import { Input } from "$lib/components/ui/input";
  import { Button } from "$lib/components/ui/button";
  import CommentItem from "./+commentItem.svelte";

  import { getIdToken } from "firebase/auth";
  import { auth } from "../firebase.js";
  import axios from "axios";

  import { selectedVideoId } from "$lib/stores/selectedVideoId";
  import { onDestroy } from "svelte";

  //data
  import { cachedComments } from "$lib/stores/dataStore";
  import { showNotification } from "$lib/stores/notificationStore";
  import { comment } from "postcss";
  import { page } from "$app/stores";
  import { nextPageTokenStoreComment } from "$lib/stores/dataStore";
  import { API_BASE_URL } from "$lib/api.js";

  let videoId = "";
  let commentData = [];
  let loading = false;

  async function fetchComments(page_token) {
    console.log(page_token);
    loading = page_token === null; // when we want more comments, it shouldn't hide the ones already there
    const user = auth.currentUser;
    let idToken = null;

    if (user) {
      idToken = await getIdToken(user);
    } else {
      console.log("User not logged in");
      return;
    }

    const response = await axios.get(`${API_BASE_URL}/get_comments`, {
      params: {
        video_id: videoId,
        next_page_token: page_token,
      },
      headers: {
        Authorization: `Bearer ${idToken}`,
        "Content-Type": "application/json",
      },
    });

    if (page_token === null) {
      commentData = [];
    }

    let response_data_comments = response.data.comments !== undefined ? response.data.comments : [];

    commentData = [...commentData, ...response_data_comments];
    $nextPageTokenStoreComment = response.data.next_page_token;
    cachedComments.set(commentData);

    if (commentData.length === 0) {
      showNotification("no scam comments found", "info");
    }
    loading = false;
  }

  // subscriptions to stores
  if ($cachedComments !== null) {
    commentData = $cachedComments;
  } else {
    $nextPageTokenStoreComment = null; // should be only reset to null on reload, and that is also when the comments get erased
  }

  // this is used to fetch comments when clicking on videoItem fetch comments button
  let unsubscribe;
  unsubscribe = selectedVideoId.subscribe((value) => {
    videoId = value;
    if (value !== null && $cachedComments === null) {
      fetchComments(null);
      console.log("fetching new comments from null");
    }
  });

  onDestroy(() => {
    unsubscribe(); // Clean up subscription when component is destroyed
    commentData = [];
    videoId = "";
    console.log("getting destroyed");
  });
</script>

<div class="flex flex-col">
  <div class="flex flex-row justify-around min-w-[30vw]">
    <Input bind:value={videoId} placeholder="Enter videoId" class="w-full px-4 py-2 m-2 border border-gray-300 rounded" />
    <Button on:click={() => fetchComments(null)} class="w-full m-2">Fetch Comments</Button>
  </div>
  <div class="w-[40vw] h-[80vh] overflow-y-auto border border-gray-300 rounded mx-2" id="videoDataContainer">
    <!-- {#if commentData.length === 0}
      {#if loading}
        <div class="flex items-center justify-center h-full text-gray-500">Loading...</div>
      {:else}
        <div class="flex items-center justify-center h-full text-gray-500">Please request data</div>
      {/if}
    {:else} -->
    <!-- Render CommentItem components when data is loaded -->
    <!-- {#each commentData as comment}
        <CommentItem {comment} moderationEffect={"rejected"} />
      {/each}
    {/if} -->

    {#if loading}
      <div class="flex items-center justify-center h-full text-gray-500">Loading...</div>
    {:else if commentData.length !== 0}
      <!-- Render CommentItem components when data is loaded -->
      {#each commentData as comment}
        <CommentItem {comment} moderationEffect={"rejected"} />
      {/each}
    {:else}
      <div class="flex items-center justify-center h-full text-gray-500">Please request data</div>
    {/if}

    {#if $nextPageTokenStoreComment !== null && !loading && commentData.length !== 0}
      <div class="flex justify-center m-2">
        <Button on:click={() => fetchComments($nextPageTokenStoreComment)} class="w-48 bg-gray-100 text-black border border-black ">Load more</Button>
      </div>
    {/if}
  </div>
</div>
