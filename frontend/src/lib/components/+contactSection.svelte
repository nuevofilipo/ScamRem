<script>
  import Button from "./ui/button/button.svelte";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  let name = writable("");
  let email = writable("");
  let message = writable("");
  let formAction = "https://formsubmit.co/579475dff0078dfceb0032894b2bc8d8"; // Replace with your actual email
</script>

<!-- Contact Section Container -->
<div class="w-full px-6 py-12 flex flex-col md:flex-row items-center justify-evenly rounded-2xl border border-black">
  <!-- Left Side: Call-to-action -->
  <h1 class="text-6xl font-bold">
    Got some questions?
    <br />Contact me!
  </h1>

  <!-- Right Side: Contact Form -->
  <div class="md:w-1/2 bg-gray-900 text-black p-8 rounded-lg">
    <form action={formAction} method="POST" class="space-y-4">
      <!-- Hidden field to disable captcha -->
      <input type="hidden" name="_captcha" value="false" />

      <!-- Name -->
      <input
        type="text"
        name="name"
        bind:value={$name}
        placeholder="Your Name"
        required
        class="w-full px-4 py-3 bg-gray-100 border border-gray-600 rounded focus:outline-none focus:border-black font-medium"
      />

      <!-- Email -->
      <input
        type="email"
        name="email"
        bind:value={$email}
        placeholder="Your Email"
        required
        class="w-full px-4 py-3 bg-gray-100 border border-gray-600 rounded focus:outline-none focus:border-black font-medium"
      />

      <!-- Message -->
      <textarea
        name="message"
        rows="5"
        bind:value={$message}
        placeholder="Your Message"
        required
        class="w-full px-4 py-3 bg-gray-100 border border-gray-600 rounded focus:outline-none focus:border-black font-medium"
      ></textarea>

      <!-- Submit Button -->
      <Button type="submit" class="px-6 py-3 bg-purple-300 text-black hover:bg-purple-400 focus:outline-none font-semibold">Send Message</Button>
    </form>
  </div>
</div>
