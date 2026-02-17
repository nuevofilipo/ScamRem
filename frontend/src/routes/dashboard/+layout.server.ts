
import { API_BASE_URL } from "$lib/api";
import { redirect } from "@sveltejs/kit";

export const load = async ({ locals, cookies, url }) => {
  const user = locals.user;
  const subscriptionCookie = cookies.get("subscription");
  
  let subscriptionStatus = false;

  if (!subscriptionCookie){
    const res = await fetch(`${API_BASE_URL}/check-subscription?userId=${user.uid}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" }, // This header isn't necessary for GET but can be left in
    });

    const data = await res.json();
    const subscription_status_on_db = data.subscription_status;
    const subscription_end_date = new Date(data.subscription_end);
    
    if(subscription_status_on_db == "inactive"){
      subscriptionStatus = false;
    } else if(subscription_status_on_db == "active"){
      subscriptionStatus = true;
    } else{
      const today = new Date();
      subscriptionStatus = today <= subscription_end_date;
    }
    // set cookie
    const expiresIn = 60 * 60 * 24 * 5 * 1000; // 5 days

    cookies.set("subscription", JSON.stringify({ value: String(subscriptionStatus), end_time: subscription_end_date}), {
      httpOnly: true,
      secure: true,
      maxAge: expiresIn,
      path: "/"
    });

  } else{
    const data = JSON.parse(subscriptionCookie);
    const subscription_end_date = new Date(data.end_time)
    const today = new Date();
    // console.log("data value: ", data.value);
    // console.log("end date", data.end_time);
    // console.log(today <= subscription_end_date);

  
    subscriptionStatus = data.value =="true" && (today <= subscription_end_date);
  }


  if (!subscriptionStatus && url.pathname != "/dashboard/subscription"){
    console.log("subscription cookie forbids access: ", subscriptionStatus);
    throw redirect( 303, "/dashboard/subscription");
  } else{
    console.log("subscription cookie gives access: ", subscriptionStatus);
  }

  return {};
};
