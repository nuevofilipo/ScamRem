<script lang="ts">
  import { goto } from "$app/navigation";
  // import VideoSection from "$lib/components/+videoSection.svelte";
  // import CommentSection from "$lib/components/+commentSection.svelte";
  import RemovedComments from "$lib/components/+removedComments.svelte";
  import { subscription, user } from "$lib/stores/authStore.js";
</script>

<div class="flex-grow flex flex-row justify-center items-center space-y-8 px-[5%] pt-4" id="content section">
  <div class="h-auto flex flex-row items-start" id="content wrapper">
    <RemovedComments />
  </div>
</div>
