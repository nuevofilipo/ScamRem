<script lang="ts">
  import { subscription, user } from "$lib/stores/authStore";
  import ProfileSection from "$lib/components/+profileSection.svelte";
  import { channelNameStore } from "$lib/stores/dataStore.js";
  import { goto } from "$app/navigation";

  export let data;
  $: {
    if (data.user) {
      // User is logged in, you can do something with the data$
      channelNameStore.set(data.items);
      console.log("Channel name:", data.items);
    } else {
      // Redirect to login or handle unauthenticated state
      // For example: goto('/login')
      console.log("not logged in yet");
    }
  }
</script>

<div class="flex-grow flex flex-row justify-center items-center space-y-8 px-[5%] pt-4" id="content section">
  <div class="h-auto flex flex-row items-start" id="content wrapper">
    <ProfileSection />
  </div>
</div>
