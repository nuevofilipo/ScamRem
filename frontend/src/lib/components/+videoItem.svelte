<script>
  import { Button } from "$lib/components/ui/button";
  import { cachedComments } from "$lib/stores/dataStore";
  export let video;
  import { selectedVideoId } from "$lib/stores/selectedVideoId";

  function selectThisId() {
    // selectedVideoId.set(video.video_id + "_update");
    $cachedComments = null;
    selectedVideoId.set(video.video_id);
  }
</script>

<div class="p-3 border border-black rounded m-2">
  <p class="font-bold">{@html video.video_title}</p>

  <div class="flex items-center w-full justify-between">
    <p class="font-light text-sm">id: {video.video_id}</p>
    <Button on:click={selectThisId} class="h-8">Fetch Comments</Button>
  </div>
</div>
