<script>
  import Button from "./ui/button/button.svelte";
</script>

<h1 class="text-5xl font-bold">Pricing:</h1>

<!-- Floating Box -->
<div class="flex flex-row items-center justify-evenly w-full">
  <div class="flex justify-center h-full">
    <div
      class="bg-purple-100 rounded-3xl p-8 w-full max-w-md text-center
               mx-4 md:mx-0"
    >
      <h3 class="text-4xl font-semibold mb-6">Beta Phase</h3>
      <p class="text-3xl font-bold mb-6">$19<span class="text-xl font-normal">/month</span></p>

      <p class="text-lg mb-8">AI Filtering of comments and moderation from inside the tool.</p>

      <!-- Custom Button element with Tailwind classes -->
      <Button href="/login" class="mt-4 text-xl px-7 py-6 font-medium rounded-full ">get started</Button>
    </div>
  </div>

  <div class="flex justify-center">
    <div
      class="bg-green-100 rounded-3xl p-8 w-full max-w-md text-center
               mx-4 md:mx-0"
    >
      <h3 class="text-4xl font-semibold mb-6">Finished Product</h3>
      <p class="text-3xl font-bold mb-6">$tba<span class="text-xl font-normal">/month</span></p>

      <p class="text-lg mb-8">
        AI Filtering of comments and moderation from inside the tool.
        <br />Automatic supervision of videos 24/7 and automatic removal of scam comments.
        <br />
      </p>

      <!-- Custom Button element with Tailwind classes -->
      <h2 class="text-2xl font-bold">Not available yet</h2>
    </div>
  </div>
</div>
