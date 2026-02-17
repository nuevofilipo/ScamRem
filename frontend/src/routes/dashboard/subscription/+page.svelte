<script>
  import { goto } from "$app/navigation";
  import { API_BASE_URL } from "$lib/api";
  import { Button } from "$lib/components/ui/button";
  import { subscription, user } from "$lib/stores/authStore";

  async function setSubscriptonCookie() {
    const response = await fetch("/dashboard/subscription", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ value: "true", end_time: "2025-03-16" }),
    });
  }

  async function setSubscriptonCookieFalse() {
    const response = await fetch("/dashboard/subscription", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ value: "false", end_time: "2025-03-16" }),
    });
  }

  async function checkSub() {
    const res = await fetch(`${API_BASE_URL}/check-subscription?userId=${$user.uid}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" }, // This header isn't necessary for GET but can be left in
    });

    const data = await res.json();
    let subscription_status = data.subscription_status;
    let end_time = data.subscription_end;

    console.log("subscription_status: ", subscription_status);
    console.log("end_time: ", end_time);
  }
</script>

<div class="flex-grow flex flex-row justify-center items-center space-y-8 px-[5%] pt-4" id="content section">
  <div class="flex-grow flex flex-row justify-center items-center space-y-8 px-[5%] pt-4" id="content section">subscription logic</div>
  <Button on:click={setSubscriptonCookie}>set cookie</Button>
  <Button on:click={setSubscriptonCookieFalse}>set cookie to false</Button>
  <Button on:click={checkSub}>check sub</Button>
</div>
