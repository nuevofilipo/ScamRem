<script lang="ts">
  import "../app.css";
  import { Button } from "$lib/components/ui/button";

  import { app, auth } from "../lib/firebase"; // adjust the path to your firebase.js
  import { signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, type AuthError } from "firebase/auth";
  import { subscription, user } from "../lib/stores/authStore";
  import { onMount } from "svelte";
  import Notification from "$lib/components/+notification.svelte";

  // data
  import { cachedRemovedComments } from "$lib/stores/dataStore";
  import { cachedComments } from "$lib/stores/dataStore";
  import { cachedVideos } from "$lib/stores/dataStore";

  // routing
  import { goto } from "$app/navigation";

  // fonts
  import "@fontsource/covered-by-your-grace";

  let errorMessage = "";
  let isMobile = false;

  async function logout() {
    try {
      await signOut(auth); // Sign out from Firebase
      await fetch("/auth/logout", { method: "POST" }); // Remove session cookie from backend
      resetData();

      console.log("User logged out");

      // Use `goto()` to navigate, then force a reload to clear stale session data
      goto("/", { replaceState: true }).then(() => {
        location.reload();
      });
    } catch (error) {
      console.error("Logout error:", error);
    }
  }

  //  listeners
  onMount(() => {
    const handleBeforeUnload = () => {
      resetData();
    };
    const checkScreenSize = () => (isMobile = window.innerWidth < 768);
    checkScreenSize();
    window.addEventListener("resize", checkScreenSize);
    window.addEventListener("beforeunload", handleBeforeUnload);

    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
      window.removeEventListener("resize", checkScreenSize);
    };
  });

  function resetData() {
    cachedRemovedComments.set(null);
    cachedComments.set(null);
    cachedVideos.set(null);
  }
  //bg-gradient-to-b from-blue-50 via-pink-50 to-white
</script>

{#if isMobile}
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-80 text-white text-2xl p-6">Please use a larger screen for the best experience.</div>
{/if}

<Notification />
<div class="mx-auto flex flex-col min-h-screen">
  <header class="flex justify-between items-center py-5 px-[5%]">
    <div class="logo">
      {#if $user}
        <a id="logo" href="/dashboard" class="text-5xl">scam rem</a>
      {:else}
        <a id="logo" href="/" class="text-5xl">scam rem</a>
      {/if}
    </div>
    <nav class="space-x-6">
      {#if !$user}
        <a href="/#pricingSection" class="text-xl font-medium">pricing</a>
        <a href="/#contactSection" class="text-xl font-medium">contact</a>
      {/if}

      {#if $user}
        <a href="/dashboard" class="text-xl font-medium">my videos</a>
        <a href="/dashboard/removedComments" class="text-xl font-medium">removed comments</a>
        <a href="/dashboard/profilePage" class="text-xl font-medium">my profile</a>
        <Button on:click={logout} class="bg-gray-300 text-black border border-black hover:bg-red-200">Logout</Button>
      {/if}
    </nav>
  </header>

  <slot />
</div>

<style>
  .logo {
    font-family: "Covered By Your Grace", cursive;
  }
</style>
