from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials, auth, firestore
from functools import wraps
from dotenv import load_dotenv
import os
from google_auth_oauthlib.flow import InstalledAppFlow, Flow

import json
import urllib.parse

load_dotenv()
app = Flask(__name__)
CORS(app)


cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)


from viewComments import (
    fetch_youtube_comments,
    moderate_single_comment,
    gpt_process_batched_comments,
    get_youtube_videos,
    save_comment_to_db,
    fetch_removed_comments,
    SCOPES,
    OAuthRequired,
    RAILWAY_URL,
)

yt_api_key = os.getenv("YT_TECH4_API_KEY")
yt_orlando_key = os.getenv("YT_FO_API_KEY")


# security function
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the ID token from the request headers
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "No authentication token provided"}), 401

        try:
            # Extract the token
            token = auth_header.split("Bearer ")[1]
            # Verify the token
            decoded_token = auth.verify_id_token(token, clock_skew_seconds=5)
            # Add the user ID to the request
            request.user_id = decoded_token["uid"]
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Auth error: {e}")
            return jsonify({"error": "Invalid authentication token"}), 401

    return decorated_function


# Modified main function to return comments
@app.route("/get_comments", methods=["GET"])
@require_auth
def api_get_comments():
    video_id = request.args.get("video_id")
    next_page_token = request.args.get("next_page_token")

    try:
        comment_data, new_page_token = fetch_youtube_comments(
            video_id, yt_api_key, next_page_token=next_page_token
        )
        processed_comments = gpt_process_batched_comments(comment_data)
        comment_dicts = [comment.to_dict() for comment in processed_comments]

        response = {"comments": comment_dicts, "next_page_token": new_page_token}
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/get_youtube_videos", methods=["GET"])
@require_auth
def api_get_youtube_video():
    channel_name = request.args.get("channel_name")
    next_page_token = request.args.get("next_page_token")

    # Fetch comments using your function
    youtube_videos, new_page_token = get_youtube_videos(
        yt_api_key, channel_name, 20, next_page_token
    )
    # somehow return the next page token
    videos_dicts = [video.to_dict() for video in youtube_videos]
    response = {"videos": videos_dicts, "next_page_token": new_page_token}
    return jsonify(response)


# Moderate a single comment via POST
@app.route("/moderate_comment", methods=["POST"])
@require_auth
def api_moderate_one_comment():
    data = request.get_json()
    comment_id = data.get("comment_id")
    comment = data.get("mycomment")
    uid = request.user_id

    moderation_status = data.get("moderation_status")
    try:
        message = moderate_single_comment(comment_id, uid, moderation_status)
        # message = "Comment Moderated"
        saving_message = save_comment_to_db(uid, comment, moderation_status)
        return jsonify(
            {"status": "success", "message": message, "saving_msg": saving_message}
        )
    except OAuthRequired as e:
        return e.to_json()
    except Exception as e:
        print(f"error: {str(e)}")
        return jsonify(
            {"status": "error", "message": "an error occurred when moderating comment"}
        )


@app.route("/fetch_removed_comments", methods=["GET"])
@require_auth
def api_fetch_removed_comments():
    uid = request.user_id
    comments = fetch_removed_comments(uid)
    return jsonify(comments)


@app.route("/fetch_channel_name", methods=["Get"])
@require_auth
def api_fetch_channel_name():
    print("in fetch channel name inside python")
    db = firestore.client()

    uid = request.user_id
    print(f"uid: {uid}")

    try:
        channel_doc = (db.collection("users").document(uid)).get()

        channel_name = None
        if channel_doc.exists:
            channel_name = channel_doc.to_dict().get("channel_name")

        return jsonify({"channel_name": f"{channel_name}"})
    except Exception as e:
        print("in except section")
        return jsonify({"error message": str(e)})


@app.route("/set_channel_name", methods=["Post"])
@require_auth
def set_fetch_channel_name():
    db = firestore.client()
    data = request.get_json()
    channel_name = data.get("channel_name")
    uid = request.user_id

    print(f"channel name: {channel_name}")

    try:
        channel_doc_ref = db.collection("users").document(uid)
        channel_doc_ref.set({"channel_name": channel_name}, merge=True)
        return jsonify({"status": "success setting new channel name"})
    except Exception as e:
        return jsonify({"status": "error setting new channel name", "message": str(e)})


@app.route("/oauth/callback")
def oauth_callback():
    state = request.args.get("state")  # This now contains user_id
    code = request.args.get("code")

    if not state or not code:
        return "Error: Missing state or code", 400

    try:
        # Decode the state and extract user_id
        state_data = json.loads(urllib.parse.unquote(state))  # Decode JSON state
        user_id = state_data.get("user_id")
        if not user_id:
            return "Error: Missing user ID", 400
    except Exception as e:
        print(f"Error decoding state: {e}")
        return "Error: Invalid state parameter", 400

    db = firestore.client()
    user_ref = db.collection("users").document(user_id)  # Use extracted user_id

    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
        redirect_uri=f"{RAILWAY_URL}/oauth/callback",
        state=state,
    )

    try:
        flow.fetch_token(code=code)
    except Exception as e:
        print(f"Token exchange failed: {e}")
        return "OAuth token exchange failed", 400

    creds = flow.credentials

    # Save the token in Firestore for this user
    user_ref.set({"youtube_token": creds.to_json()}, merge=True)

    return "Authentication successful! You can close this tab and moderate your comments now."


if __name__ == "__main__":
    app.run(debug=True)
