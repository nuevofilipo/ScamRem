<script>
  import { user } from "$lib/stores/authStore";
  import { Button } from "$lib/components/ui/button";
  import axios from "axios";
  import { getIdToken, sendEmailVerification } from "firebase/auth";
  import { auth } from "../firebase.js";
  import { fetchChannelName } from "../api.js";
  import { channelNameStore } from "$lib/stores/dataStore.js";
  import { verifyBeforeUpdateEmail, updatePassword } from "firebase/auth";
  import Notification from "./+notification.svelte";
  import { showNotification } from "$lib/stores/notificationStore.js";

  import { setChannelName } from "$lib/api.js";

  let channelName = "";
  let email = "";
  $: email = $user !== null ? $user.email : "";

  let password = "";

  // welcoming section
  let emoji;
  let timeOfDay = "";

  $: channelName = $channelNameStore;

  const hours = new Date().getHours();
  if (hours < 12 && hours >= 6) {
    emoji = "☀️"; // Morning emoji
    timeOfDay = "Morning";
  } else if (hours < 18 && hours >= 12) {
    emoji = "🌤️"; // Afternoon emoji
    timeOfDay = "Afternoon";
  } else if (hours < 24 && hours >= 18) {
    emoji = "🌙"; // Evening emoji
    timeOfDay = "Evening";
  } else {
    emoji = "🌚"; // Night emoji
    timeOfDay = "Night";
  }

  async function changeEmail() {
    const user = auth.currentUser;
    if (user && email !== user.email) {
      try {
        await verifyBeforeUpdateEmail(user, email);
        console.log("Verification email sent to new email. Please confirm before the change takes effect.");
        showNotification("Verification email sent to new email. Please confirm before the change takes effect.", "success");
      } catch (error) {
        console.error("Error updating email:", error.message);
        showNotification(error.message, "error");
      }
    } else {
      showNotification("Enter a new email", "info");
    }
  }

  async function changePassword() {
    const user = auth.currentUser;
    if (user && password) {
      try {
        await updatePassword(user, password);
        console.log("Password updated successfully");
        showNotification("Password updated successfully", "success");
      } catch (error) {
        console.error("Error updating password:", error.message);
        showNotification(error.message, "error");
      }
    }
  }

  async function saveChanges() {
    await changeEmail();
    await changePassword();
  }

  // notification showing logic
  let message = "hello you should go to sleep";
</script>

<div class="flex flex-col items-center justify-around">
  <p class="font-semibold text-lg p-4">Good {timeOfDay}, {email} {emoji}</p>

  <div class="bg-white p-6 rounded-lg w-[25vw] min-w-[250px] border border-black">
    <h2 class="text-2xl font-semibold mb-6 text-center">Account Settings</h2>
    <form class="space-y-5">
      <div>
        <label class="block text-sm font-medium text-gray-700">Email</label>
        <input
          autocomplete="off"
          bind:value={email}
          class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-gray-500 focus:border-gray-500"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">New Password</label>
        <input
          autocomplete="new-password"
          type="password"
          bind:value={password}
          class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-gray-500 focus:border-gray-500"
        />
      </div>
      <Button class="w-full border border-black" on:click={saveChanges}>update email & password</Button>
      <div>
        <label class="block text-sm font-medium text-gray-700">Channel Name</label>
        <input
          type="text"
          bind:value={channelName}
          class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-gray-500 focus:border-gray-500"
        />
      </div>
      <Button class="w-full border border-black" on:click={() => setChannelName(channelName)}>update channel name</Button>
    </form>
  </div>
</div>
