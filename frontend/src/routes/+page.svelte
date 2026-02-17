<script lang="ts">
  import VideoSection from "$lib/components/+videoSection.svelte";
  import CommentSection from "$lib/components/+commentSection.svelte";

  import { subscription, user } from "$lib/stores/authStore";
  import HeroSection from "$lib/components/+heroSection.svelte";
  import SecondSection from "$lib/components/+secondSection.svelte";
  import { channelNameStore } from "$lib/stores/dataStore.js";
  import PricingSection from "$lib/components/+pricingSection.svelte";
  import ContactSection from "$lib/components/+contactSection.svelte";
  import FooterSection from "$lib/components/+footerSection.svelte";
  import { goto } from "$app/navigation";

  // for handling data loading:
</script>

<div class="flex flex-col">
  <div class="w-full h-[70vh] flex items-center justify-center">
    <HeroSection />
  </div>
  <div class="w-full h-[80vh] flex items-center justify-center px-[5%]">
    <SecondSection />
  </div>
  <div id="pricingSection" class="w-full h-[80vh] flex flex-col items-center justify-evenly px-[5%]">
    <PricingSection />
  </div>
  <div id="contactSection" class="w-full h-[60vh] flex flex-row items-center justify-evenly px-[5%]">
    <ContactSection />
  </div>
  <div id="footerSection" class="w-full flex flex-column items-center justify-evenly px-[5%] py-10">
    <FooterSection />
  </div>
</div>
