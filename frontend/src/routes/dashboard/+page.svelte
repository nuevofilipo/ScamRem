<script lang="ts">
  import VideoSection from "$lib/components/+videoSection.svelte";
  import CommentSection from "$lib/components/+commentSection.svelte";
  import { channelNameStore } from "$lib/stores/dataStore.js";

  // for handling data loading:

  export let data;
  $: {
    if (data.user) {
      channelNameStore.set(data.items);
      console.log("Channel name:", data.items);
    } else {
      console.log("not logged in yet");
    }
  }
</script>

<div class="flex-grow flex flex-row justify-center items-center space-y-8 px-[5%] pt-4" id="content section">
  <div class="h-auto flex flex-row items-start" id="content wrapper">
    <VideoSection />
    <CommentSection />
  </div>
</div>
