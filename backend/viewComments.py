# google imports
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.oauth2.credentials import Credentials

# other imports
from openai import OpenAI
import pandas as pd
import time
import os
import json
from dotenv import load_dotenv
import requests
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore

import urllib.parse

RAILWAY_URL = "https://" + os.getenv("RAILWAY_PUBLIC_DOMAIN", "127.0.0.1:5000")


# Define the OAuth2 scope for YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
load_dotenv()


def authenticate_youtube(user_id):
    db = firestore.client()
    creds = None

    # Try to load the OAuth2 token from Firebase
    user_ref = db.collection("users").document(user_id)
    user_data = user_ref.get().to_dict()

    if user_data and "youtube_token" in user_data:
        try:
            token_info = json.loads(user_data["youtube_token"])

            creds = Credentials.from_authorized_user_info(token_info, SCOPES)

            # If refresh_token is missing, force re-authentication
            if not creds.refresh_token:
                print("No refresh token found. Initiating OAuth flow.")
                creds = get_new_credentials_remote(user_id)

        except Exception as e:
            print(f"Error in authenticate_youtube: {str(e)}")
            creds = get_new_credentials_remote(user_id)

    # If no valid token, start the OAuth flow to get one
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            user_ref.update({"youtube_token": creds.to_json()})  # save the new token
        else:
            creds = get_new_credentials_remote(user_id)

    # Validate the token by making a simple request
    youtube = build("youtube", "v3", credentials=creds)
    try:
        youtube.channels().list(part="id", mine=True).execute()  # Test request
    except Exception as e:
        print("Token is invalid or permissions revoked. Re-authenticating.")
        creds = get_new_credentials_remote(user_id)
        youtube = build("youtube", "v3", credentials=creds)
        user_ref.update({"youtube_token": creds.to_json()})  # Save new token

    return youtube


# works locally
def get_new_credentials_local(user_id):
    """Force OAuth flow and save new credentials."""
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    flow.run_local_server(
        port=8080, prompt="consent"
    )  # Force consent to get refresh_token
    creds = flow.credentials

    db = firestore.client()
    user_ref = db.collection("users").document(user_id)

    user_ref.set({"youtube_token": creds.to_json()}, merge=True)
    print("New token saved to Firestore.")

    return creds


# works remotely
def get_new_credentials_remote(user_id):
    """Start OAuth flow and guide user to authenticate manually."""
    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
        redirect_uri=f"{RAILWAY_URL}/oauth/callback",
    )

    # Encode user_id in the state parameter
    state_data = json.dumps({"user_id": user_id})  # Convert user_id to a string
    encoded_state = urllib.parse.quote(state_data)  # URL encode it

    auth_url, state = flow.authorization_url(
        prompt="consent", access_type="offline", state=encoded_state
    )

    print(f"Go to this URL to authorize: {auth_url} \n")
    raise OAuthRequired(auth_url)


class OAuthRequired(Exception):
    """Exception raised when OAuth authentication is required. This exception then propels down and gets checked for in the js frontend"""

    def __init__(self, url):
        super().__init__("oauth")
        self.url = url

    def __str__(self):
        return f"{super().__str__()}"

    def to_json(self):
        # Converts the exception to a dictionary and then serializes it to JSON
        return json.dumps(
            {
                "message": str(self),  # Uses the string representation of the exception
                "url": self.url,
            }
        )


def fetch_youtube_comments(video_id, api_key, max_results=20, next_page_token=None):
    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        pageToken=next_page_token,  # Add page token for pagination
        order="relevance",
    )

    response = request.execute()
    listOfComments = []

    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]
        author = comment["authorDisplayName"]
        text = comment["textDisplay"]

        authorChannelId = comment["authorChannelId"]["value"]
        channelId = item["snippet"]["channelId"]

        if not authorChannelId == channelId:
            listOfComments.append(item)

    # Return comments and the nextPageToken if more comments are available
    next_page_token = response.get("nextPageToken", None)
    return listOfComments, next_page_token


def get_gpt4_response(
    comments: str,
) -> str:
    openai_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_key)

    data_embedding = """
    AWS21T will change the crypto game forever!
    Let’s go NVDAH19$ token
    Kardden Token and amazon signed a partnership. It will blow up once it hits mainstream.
    first the dog, then the car, then the house, but eventually got my XAI550K
    I will be forever grateful to you, you changed my entire life and I will continue to preach on your behalf for the whole world to hear you saved me from huge financial debt with just a small investment, thank you Michelle Stewart.
    thank you mrs mikela, because of you my children can go to college, you are a life saver
    Bought AWS87T after watching your video, super excited!

    IIsis Gonzalez expertise is truly commendable.
    She has this skill of making complex crypto concepts easy to understand.

    Thanks for sharing such valuable information! I need some advice: I have a SafePal wallet with USDT, and I have the seed phrase. (air carpet target dish off jeans toilet sweet piano spoil fruit essay). How should I go about transferring them to Binance?
    """

    instruction = """
    You will be provided a list of multiple youtube comments and the amount of likes and replies they got.
    You have to decide if the comment is a scam or not!

    for every single comment output SCAM or LEGIT, and only that!

    in the end you will return multiple times SCAM or LEGIT based on the amount of comments you have received.
    """

    prompt = f"""
    {instruction}

    Data Embedding: {data_embedding}

    YouTube Comments: {comments}
    """

    completion = client.chat.completions.create(
        model="gpt-4o",  # Ensure this is the correct model name you want to use
        messages=[{"role": "user", "content": prompt}],
    )

    return completion.choices[0].message.content


# best performing accuracy above 85 percent
def get_gpt4_response2(
    comments: str,
) -> str:
    openai_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_key)

    data_embedding = """
    Got my bags full of XAI44K$ and SHIB. No way I’m missing this 15x run. Real FOMO hours! -> SCAM

    I tell myself I follow this channel for the crypto advice but let's be honest, it's Alex's on-point insults and the half-assed automated scambots that constantly try to steal money I don't have. -> LEGIT

    I thought that crypto and bitcoin trading would only be possible for highly educated and math savvy people. But with the help of Amanda Smith I was able to earn 2 btc per week. Highly recommended. Msg on TG -> SCAM

    """

    instruction = """
    You will be provided a list of multiple youtube comments and the amount of likes and replies they got.
    You have to decide if the comment is a scam or not!

    for every single comment output SCAM or LEGIT, and only that!
    in the end you will return multiple times SCAM or LEGIT based on the amount of comments you have received.

    some tips:
    - most comments recommending a not well known cryptocoin are scams
    - most comments mentioning some expert person are scams
    - most comments selling something, like a book are scams

    you also get provided a data embedding that shows some examples of comments and if they are scams or not.
    """

    prompt = f"""
    {instruction}

    Data Embedding: {data_embedding}

    YouTube Comments: {comments}
    """

    completion = client.chat.completions.create(
        model="gpt-4o",  # Ensure this is the correct model name you want to use
        messages=[{"role": "user", "content": prompt}],
    )

    return completion.choices[0].message.content


def get_gpt4_response3(
    comments: str,
) -> str:
    openai_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_key)

    data_embedding = """
    """

    instruction = """
    You will be provided a list of multiple youtube comments and the amount of likes and replies they got.
    You have to decide if the comment is a scam or not!

    for every single comment output SCAM or LEGIT, and only that!
    in the end you will return multiple times SCAM or LEGIT based on the amount of comments you have received.
    """

    prompt = f"""
    {instruction}

    YouTube Comments: {comments}
    """

    completion = client.chat.completions.create(
        model="gpt-4o",  # Ensure this is the correct model name you want to use
        messages=[{"role": "user", "content": prompt}],
    )

    return completion.choices[0].message.content


#! comment and video classes
class Comment:
    comment_id = None
    comment_text = None
    comment_like_count = None
    comment_reply_count = None
    comment_status = None
    already_moderated = False

    def __init__(
        self, comment_id, comment_text, comment_status, like_count=0, reply_count=0
    ):
        self.comment_id = comment_id
        self.comment_text = comment_text
        self.comment_status = comment_status
        self.comment_like_count = like_count
        self.comment_reply_count = reply_count

    def __str__(self):
        return (
            f"Comment ID: {self.comment_id}\n"
            f"Comment Text: {self.comment_text}\n"
            f"Status: {self.comment_status}\n"
            f"Like Count: {self.comment_like_count}\n"
            f"Reply Count: {self.comment_reply_count}\n"
        )

    def to_dict(self):
        return {
            "comment_id": self.comment_id,
            "comment_text": self.comment_text,
            "comment_status": self.comment_status,
            "comment_like_count": self.comment_like_count,
            "comment_reply_count": self.comment_reply_count,
            "already_moderated": self.already_moderated,
        }


class YoutubeVideo:
    video_id = None
    video_title = None
    published_at = None

    def __init__(self, video_id, video_title, published_at):
        self.video_id = video_id
        self.video_title = video_title
        # self.published_at = published_at
        self.published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")

    def __str__(self):
        return (
            # f"Video ID: {self.video_id}\n"
            f"Video Title: {self.video_title}\n"
            # f"Published At: {self.published_at}\n"
        )

    def to_dict(self):
        return {
            "video_id": self.video_id,
            "video_title": self.video_title,
            "published_at": self.published_at,
        }


#! batched comments together in one prompt
def gpt_process_batched_comments(comment_data):
    prepped_data = []  # data in string format
    comment_objects = []

    comment_counter = 0

    for item in comment_data:
        comment_obj = item["snippet"]["topLevelComment"]["snippet"]
        comment_text = comment_obj["textDisplay"]
        like_count = comment_obj["likeCount"]
        reply_count = item["snippet"]["totalReplyCount"]

        new_comment_obj = Comment(
            item["id"], comment_text, "NEUTRAL", like_count, reply_count
        )
        comment_objects.append(new_comment_obj)

        prepped_data.append(
            (
                f"comment{str(comment_counter)}: " + comment_text,
                "like_count: " + str(like_count),
                "reply_count: " + str(reply_count),
            )
        )
        comment_counter += 1

    response = get_gpt4_response2(prepped_data)
    response = response.split("\n")

    scamComments = []

    comment_counter = 0
    for item in response:
        if "SCAM" in item:
            comment_objects[comment_counter].comment_status = "SCAM"
            scamComments.append(comment_objects[comment_counter])
        elif "LEGIT" in item:
            comment_objects[comment_counter].comment_status = "LEGIT"
            # scamComments.append(comment_objects[comment_counter])

        comment_counter += 1
    return scamComments


def create_comment_batches(comment_data, batch_size=10):
    print("in this function")
    batches = []

    counter = 0
    currbatch = []
    for item in comment_data:
        if counter == batch_size:
            batches.append(currbatch)
            currbatch = []
            counter = 0

        currbatch.append(item)
        counter += 1
    if currbatch != []:
        batches.append(currbatch)

    for batch in batches:
        print(len(batch))


# this uses one prompt for each comment
def separate_comments(comment_data):
    potential_scams = []

    for item in comment_data:
        comment_obj = item["snippet"]["topLevelComment"]["snippet"]
        comment = comment_obj["textDisplay"]
        like_count = comment_obj["likeCount"]
        reply_count = item["snippet"]["totalReplyCount"]

        gpt_response = get_gpt4_response(comment)
        # print(f"response: {gpt_response}, comment: {comment}")
        if gpt_response == "SCAM":
            new_comment = Comment(item["id"], comment, "SCAM")
            potential_scams.append(new_comment)
        else:
            new_comment = Comment(item["id"], comment, "LEGIT")
            potential_scams.append(new_comment)
    return potential_scams


def moderate_single_comment(comment_id, uid, moderation_status="rejected"):
    # endpoint Only works using OAuth:

    try:
        youtube = authenticate_youtube(uid)
        youtube.comments().setModerationStatus(
            id=comment_id, moderationStatus=moderation_status, banAuthor=False
        ).execute()
        print(
            f"successfully set moderation status to '{moderation_status}' for comment thread ID: {comment_id}"
        )
        return f"set moderation status to '{moderation_status}' for comment thread ID: {comment_id}"
    except OAuthRequired as e:
        raise
    except Exception as e:
        raise Exception(f"Error in moderate_single_comment: {str(e)}")


def save_comment_to_db(uid, comment, moderationStatus):
    db = firestore.client()

    # Reference to the user's moderated comments subcollection
    comment_id = comment.get("comment_id")
    if not comment_id:
        return {"status": "error", "message": "Missing comment ID"}

    # Create the document reference
    comment_ref = (
        db.collection("users")
        .document(uid)
        .collection("moderated_comments")
        .document(comment_id)
    )

    comment_data = {
        "comment_id": comment_id,
        "comment_text": comment.get("comment_text", ""),
        "comment_status": comment.get("comment_status", ""),
        "comment_like_count": comment.get("comment_like_count", 0),
        "comment_reply_count": comment.get("comment_reply_count", 0),
        "moderatedAt": firestore.SERVER_TIMESTAMP,
    }

    try:

        if moderationStatus == "rejected":
            comment_ref.set(comment_data)
        elif moderationStatus == "published":
            comment_ref.delete()
        return f"Comment processed successfully"
    except Exception as e:
        raise Exception(f"Error in save_comment_to_db: {str(e)}")


def fetch_removed_comments(uid):
    db = firestore.client()

    moderated_comments_ref = (
        db.collection("users").document(uid).collection("moderated_comments")
    )

    moderated_comments = moderated_comments_ref.stream()

    # Create a list of dictionaries to store the data
    moderated_comments_data = []

    for comment in moderated_comments:
        comment_data = comment.to_dict()
        # print(comment_data)
        comment_data["moderatedAt"] = comment_data["moderatedAt"].strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        moderated_comments_data.append(comment_data)

    # export_comments_to_json(moderated_comments_data)
    return moderated_comments_data


def export_comments_to_json(comments):
    # Fetch the moderated comments

    # Convert the data to JSON
    json_data = json.dumps(comments, indent=4)

    # Write to comments.json
    with open("comments2.json", "w") as f:
        f.write(json_data)

    print("Exported to comments2.json successfully!")


def moderate_all_comments(scam_comments_list, moderation_status="rejected"):
    # we receive a list of comment objects with their statuses
    for comment_obj in scam_comments_list:
        print(comment_obj)

        # getting user input
        while True:
            print("Do you want to moderate this comment? (y/n)")
            user_input = input().lower()  # handle Y and N
            if user_input == "y" or user_input == "n":
                break
            else:
                print("Please give input in correct format (y/n).")

        if user_input == "y":
            try:
                moderate_single_comment(comment_obj.comment_id, moderation_status)
                comment_obj.already_moderated = True
                print("Comment moderated successfully.")

            except Exception as e:
                print(f"Error in moderate_all_comments: {str(e)}")
        elif user_input == "n":
            print("Comment not moderated.")
            continue


def get_comment(comment_id):
    youtube = authenticate_youtube()
    request = youtube.comments().list(part="snippet", id=comment_id)
    response = request.execute()
    print(response)

    if "items" in response:
        for item in response["items"]:
            comment = item["snippet"]
            print(f"Comment ID: {item['id']}, Text: {comment['textDisplay']}")
    else:
        print("No comment found with this ID.")


def list_channel_videos(api_key, channel_id=None, username=None):
    if not channel_id and not username:
        raise ValueError("Either channel_id or username must be provided")

    youtube = build("youtube", "v3", developerKey=api_key)

    try:
        channels_response = (
            youtube.channels()
            .list(part="contentDetails", id=channel_id, forUsername=username)
            .execute()
        )

        if not channels_response["items"]:
            return "Channel not found."

        uploads_playlist_id = channels_response["items"][0]["contentDetails"][
            "relatedPlaylists"
        ]["uploads"]

        videos = []
        next_page_token = None

        while True:
            playlist_response = (
                youtube.playlistItems()
                .list(
                    part="snippet",
                    playlistId=uploads_playlist_id,
                    maxResults=50,
                    pageToken=next_page_token,
                )
                .execute()
            )

            videos.extend(
                [
                    {
                        "title": item["snippet"]["title"],
                        "video_id": item["snippet"]["resourceId"]["videoId"],
                        "published_at": item["snippet"]["publishedAt"],
                    }
                    for item in playlist_response["items"]
                ]
            )

            next_page_token = playlist_response.get("nextPageToken")
            if not next_page_token:
                break

        return videos

    except HttpError as e:
        return f"An HTTP error occurred: {e.resp.status} {e.content}"


def get_youtube_videos(api_key, channel_name, max_results=20, next_page_token=None):
    base_url = "https://www.googleapis.com/youtube/v3/"
    search_url = f"{base_url}search"
    videos = []

    channel_id = get_channel_id(api_key, channel_name)

    while True:
        params = {
            "key": api_key,
            "channelId": channel_id,
            "part": "snippet",
            "order": "date",
            "maxResults": 20,
            "pageToken": next_page_token,
            "type": "video",
        }

        response = requests.get(search_url, params=params)
        data = response.json()

        for item in data["items"]:
            videos.append(
                YoutubeVideo(
                    item["id"]["videoId"],
                    item["snippet"]["title"],
                    item["snippet"]["publishedAt"],
                )
            )

            if len(videos) >= max_results:
                break

        next_page_token = data.get("nextPageToken")
        if not next_page_token or len(videos) >= max_results:
            break

    return videos, next_page_token


def get_channel_id(api_key, channel_name):
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        part="id", type="channel", q=channel_name, maxResults=1
    )
    response = request.execute()

    if response["items"]:
        return response["items"][0]["id"]["channelId"]
    else:
        return "Channel not found"


if __name__ == "__main__":
    my__tech4_key = os.getenv("YT_TECH4_API_KEY")
    my_video_id = "5gJYFSJSjuM"
    # crypto_video_id = "NedUS9J4Er0"
    # alex_crypto_video_id = "plFsyObArs8"


#! Ideas: I could also automatically ban the user per button press
#! Idea: Provide the AI the title or even caption track of the video, to give it reference what the
#! video is about
