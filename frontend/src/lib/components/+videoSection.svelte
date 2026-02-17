<script>
  import { Input } from "$lib/components/ui/input";
  import { Button } from "$lib/components/ui/button";

  import VideoItem from "$lib/components/+videoItem.svelte";

  import { getIdToken } from "firebase/auth";
  import { auth } from "../firebase.js";
  import axios from "axios";
  //data
  import { cachedVideos, nextPageTokenStoreVideo } from "$lib/stores/dataStore";
  import { channelNameStore } from "$lib/stores/dataStore.js";
  import { fetchVideos } from "$lib/api.js";

  let channelName;
  // reacts to changes in channel Name
  $: channelName = $channelNameStore;

  let videoData = [];
  let next_page_token = null;

  $: next_page_token = $nextPageTokenStoreVideo;

  $: videoData = $cachedVideos !== null ? $cachedVideos : [];
</script>

<div class="flex flex-col">
  <div class="flex flex-row justify-around min-w-[30vw]">
    <!-- <Input bind:value={channelName} placeholder="Enter channelName/Tag" class="w-full px-4 py-2 m-2 border border-gray-300 rounded" /> -->
    <Button on:click={() => fetchVideos(null)} class="w-full m-2">Fetch my Videos</Button>
  </div>
  <div class="w-[40vw] h-[80vh] items-center overflow-y-auto border border-gray-300 rounded mx-2" id="videoDataContainer">
    <!-- here the videoItem Components will be loaded -->
    {#if videoData.length === 0}
      <div class="flex items-center justify-center h-full text-gray-500">Please request data</div>
    {:else}
      <!-- Render VideoItem components when data is loaded -->

      {#each videoData as video}
        <VideoItem {video} />
      {/each}
    {/if}

    <!-- load more button, only when there is more to load -->
    {#if $nextPageTokenStoreVideo !== null}
      <div class="flex justify-center m-2">
        <Button on:click={() => fetchVideos($nextPageTokenStoreVideo)} class="w-48 bg-gray-100 text-black border border-black ">Load more</Button>
      </div>
    {/if}
  </div>
</div>
