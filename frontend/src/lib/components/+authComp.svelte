<script lang="ts">
  import { Input } from "$lib/components/ui/input";
  import { Button } from "$lib/components/ui/button";

  import { app, auth } from "../firebase.js"; // adjust the path to your firebase.js
  import { signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, type AuthError, onAuthStateChanged, sendPasswordResetEmail } from "firebase/auth";
  import { fetchChannelName, fetchVideos, setChannelName } from "$lib/api.js";
  import { channelNameStore } from "$lib/stores/dataStore.js";
  import { goto } from "$app/navigation";
  import { showNotification } from "$lib/stores/notificationStore.js";
  import { user } from "$lib/stores/authStore.js";

  // You can use Svelte's bind:value instead of getting values from DOM
  let email = "";
  let password = "";
  let errorMessage = "";
  let channelName = "";
  let acceptedTerms = false;
  let signingup = false;
  let loading = false;
  let forgotPassword = false;

  async function signup() {
    try {
      if (channelName === "") {
        showNotification("Please enter a channel name", "error");
        return;
      }
      if (!acceptedTerms) {
        showNotification("Please accept the terms and conditions", "error");
        return;
      }
      loading = true;

      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const idToken = await userCredential.user.getIdToken();
      await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idToken }),
      });
      await setChannelName(channelName);
      await goto("/dashboard");
      console.log("User signed up:", userCredential.user);
    } catch (error) {
      console.error("Signup error:", (error as AuthError).message);
      errorMessage = (error as AuthError).message;
      showNotification(errorMessage, "error");
    }
    loading = false;
  }

  async function login() {
    try {
      loading = true;
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const idToken = await userCredential.user.getIdToken();
      // set saved channel name on login
      await waitForAuthState();
      await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idToken }),
      });
      await goto("/dashboard");
    } catch (error) {
      console.error("Login error:", (error as AuthError).message);
      errorMessage = (error as AuthError).message;
      showNotification(errorMessage, "error");
    }
    loading = false;
  }

  function waitForAuthState(): Promise<void> {
    return new Promise((resolve) => {
      const unsubscribe = onAuthStateChanged(auth, (user) => {
        if (user) {
          console.log("Auth state updated, user is set.");

          unsubscribe(); // Stop listening after we get a user
          resolve();
        }
      });
    });
  }

  async function resetPassword() {
    if (!email) {
      showNotification("Please enter your email address", "info");
      return;
    }

    try {
      await sendPasswordResetEmail(auth, email);
      showNotification("Password reset email sent! Check your inbox.", "success");
    } catch (error) {
      console.error("Error resetting password:", error);
      showNotification("Failed to send password reset email. Check if the email is correct.", "error");
    }
  }
</script>

<div class="flex justify-center items-center w-[25vw]">
  {#if loading}
    <div class="flex justify-center items-center w-full h-full">
      <div class="animate-spin rounded-full h-16 w-16 border-[6px] border-solid border-purple-400 border-t-transparent"></div>
    </div>
  {:else}
    <div class="w-full max-w-sm p-6 bg-white rounded-lg border border-black">
      <h2 class="text-2xl font-semibold text-center text-gray-800 mb-6">{signingup === false ? (forgotPassword === false ? "login" : "reset password") : "signup"}</h2>

      <!-- Login Form -->
      <div class="space-y-4 flex flex-col justify-center items-center">
        <Input bind:value={email} placeholder="Email" class="w-full px-4 py-2 m-2 border border-gray-300 rounded" />
        {#if !forgotPassword}
          <Input bind:value={password} type="password" placeholder="Password" class="w-full px-4 py-2 m-2 border border-gray-300 rounded" />
        {/if}

        {#if signingup}
          <Input bind:value={channelName} placeholder="your channel's name" class="w-full px-4 py-2 m-2 border border-gray-300 rounded" />
          <label class="flex items-center justify-center m-2 text-sm text-gray-500">
            <input type="checkbox" bind:checked={acceptedTerms} class="mr-2 h-4 w-4 accent-purple-400" />
            I have read and agree to the
            <a href="/privacy" class="text-purple-500 underline ml-1">Terms of Service & Privacy Policy</a>.
          </label>
          <Button on:click={signup} class="w-full m-2 bg-gray-200 text-black border border-black hover:bg-blue-200">Create Account</Button>
          <a href="/login" on:click={() => (signingup = false)} class="text-purple-500 underline text-sm m-2"> Already have an account? Log in </a>
        {:else if !forgotPassword}
          <Button on:click={login} class="w-full m-2">Login</Button>
          <a href="/login" on:click={() => (signingup = true)} class="text-purple-500 underline text-sm m-2"> Don't have an account? Sign up </a>
          <a href="/login" on:click={() => (forgotPassword = true)} class="text-purple-500 underline text-sm m-2"> Forgot your password? </a>
        {:else}
          <Button on:click={resetPassword} class="w-full m-2">Send Reset Email</Button>
          <a href="/login" on:click={() => (forgotPassword = false)} class="text-purple-500 underline text-sm m-2"> back to login </a>
        {/if}
      </div>
    </div>
  {/if}
</div>

<style>
</style>
