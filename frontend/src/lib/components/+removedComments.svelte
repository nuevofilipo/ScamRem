<script>
  import { Input } from "$lib/components/ui/input";
  import { Button } from "$lib/components/ui/button";
  import CommentItem from "./+commentItem.svelte";

  import { getIdToken } from "firebase/auth";
  import { auth } from "../firebase.js";
  import axios from "axios";

  import { cachedRemovedComments } from "$lib/stores/dataStore";
  import { fetchRemovedComments } from "$lib/api";

  let removedCommentData = [];

  $: removedCommentData = $cachedRemovedComments !== null ? $cachedRemovedComments : [];
</script>

<div class="flex flex-col">
  <div class="flex flex-row justify-around min-w-[30vw]">
    <!-- <Input bind:value={videoId} placeholder="Enter videoId" class="w-full px-4 py-2 m-2 border border-gray-300 rounded" /> -->
    <Button on:click={fetchRemovedComments} class="w-full m-2">Fetch Removed Comments</Button>
  </div>
  <div class="w-[40vw] h-[80vh] overflow-y-auto border border-gray-300 rounded mx-2" id="videoDataContainer">
    {#if removedCommentData.length === 0}
      <div class="flex items-center justify-center h-full text-gray-500">Please request data</div>
    {:else}
      <!-- Render CommentItem components when data is loaded -->
      {#each removedCommentData as comment}
        <CommentItem {comment} moderationEffect={"published"} />
      {/each}
    {/if}
  </div>
</div>
