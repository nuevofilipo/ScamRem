<script>
  import { Button } from "$lib/components/ui/button";
  export let comment;
  export let moderationEffect;
  import { getIdToken } from "firebase/auth";
  import { auth } from "../firebase.js";
  import axios from "axios";
  import { showNotification } from "$lib/stores/notificationStore.js";
  import { API_BASE_URL } from "$lib/api.js";

  let visible = true;

  async function moderateComment() {
    const user = auth.currentUser;
    let idToken = null;

    if (user) {
      idToken = await getIdToken(user);
    }

    let mycomment = {
      comment_id: comment.comment_id,
      comment_text: comment.comment_text,
      comment_status: comment.comment_status,
      comment_like_count: comment.comment_like_count,
      comment_reply_count: comment.comment_reply_count,
    };

    const response = await axios.post(
      `${API_BASE_URL}/moderate_comment`,
      {
        comment_id: comment.comment_id,
        mycomment,
        moderation_status: moderationEffect,
        uid: user.uid,
      },
      {
        headers: {
          Authorization: `Bearer ${idToken}`,
          "Content-Type": "application/json",
        },
      }
    );

    // oauth token not yet in db, run oauth flow
    if (response.data["message"] === "oauth") {
      console.log("oauth");
      const newWindow = window.open(response.data["url"], "_blank");
      if (newWindow) {
        newWindow.focus(); // Bring the new window to the foreground
      } else {
        console.error("Popup blocked! Allow popups for this site.");
        showNotification("Popup blocked! Allow popups for this site.", "error");
      }
    } else {
      // normal flow, non oauth
      showNotification(response.data["message"], response.data["status"]);
      console.log(response.data);
      if (response.data["status"] === "success") {
        visible = false;
      }
    }
  }
</script>

{#if visible}
  <div class="p-3 border border-black rounded m-2">
    <p class="font-normal">{@html comment.comment_text}</p>

    <div class="flex items-center w-full justify-between">
      <p class="font-light text-sm">
        Likes: {comment.comment_like_count} | Replies: {comment.comment_reply_count} | Status: <span class="comment-status">{comment.comment_status}</span> | <br /> ID: {comment.comment_id}
      </p>
      {#if moderationEffect === "rejected"}
        <Button on:click={moderateComment} class="h-8 ">Remove Comment</Button>
      {:else}
        <Button on:click={moderateComment} class="h-8">Approve Comment</Button>
      {/if}
    </div>
  </div>
{/if}
