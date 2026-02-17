<script>
  import FooterSection from "$lib/components/+footerSection.svelte";
  import PrivacyComponent from "$lib/components/+privacyComponent.svelte";
  import TermsComponent from "$lib/components/+termsComponent.svelte";
</script>

<div class="flex-grow flex flex-col justify-center items-center space-y-8 px-[5%] py-4" id="content section">
  <PrivacyComponent />
  <TermsComponent />
  <FooterSection />
</div>
