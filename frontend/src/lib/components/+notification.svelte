<script>
  import { notifications } from "$lib/stores/notificationStore";
  import { fade } from "svelte/transition";
</script>

<div class="fixed top-20 right-4 flex flex-col gap-2">
  {#each $notifications as { id, message, type } (id)}
    <div class="p-4 w-[350px] rounded-lg shadow-md text-white" class:bg-green-500={type === "success"} class:bg-red-500={type === "error"} class:bg-yellow-500={type === "info"} in:fade out:fade>
      {message}
    </div>
  {/each}
</div>
