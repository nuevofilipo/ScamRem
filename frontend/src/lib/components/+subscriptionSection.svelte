<script>
  import { API_BASE_URL } from "$lib/api";
  import Button from "$lib/components/ui/button/button.svelte";
  import { user } from "$lib/stores/authStore";
  import { showNotification } from "$lib/stores/notificationStore";

  async function subscribe() {
    if (!$user || !$user.uid) {
      console.error("User not logged in");
      return;
    }

    const res = await fetch(`${API_BASE_URL}/create-checkout-session`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userId: $user.uid, email: $user.email }),
    });

    const { id, url } = await res.json();
    if (url) {
      window.location.href = url;
    }
  }

  async function cancelSubscription() {
    const res = await fetch(`${API_BASE_URL}/cancel-subscription`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userId: $user.uid }),
    });

    let data = await res.json();
    showNotification(data.message, "info");
  }
</script>

<div class="flex flex-col items-center justify-around">
  <div class="flex flex-col h-full p-6 rounded-lg w-[25vw] min-w-[250px] border border-black">
    <h2 class="text-2xl font-semibold mb-6 text-center">Manage your subscription</h2>
    <Button on:click={subscribe}>Subscribe</Button>
    <Button class="my-2" on:click={cancelSubscription}>Cancel subscription</Button>
  </div>
</div>
