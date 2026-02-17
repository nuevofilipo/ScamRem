# Scamrem — AI-Powered YouTube Comment Moderation

Scamrem is a full-stack web application that helps YouTube creators detect and remove scam comments from their videos using AI. It combines GPT-4o classification with the YouTube Data API to give channel owners a one-click moderation workflow — no more manually sifting through hundreds of bot-generated crypto scams, fake endorsements, and phishing attempts.

**Live demo video is embedded on the landing page at www.scamrem.com**

---

## The Problem

YouTube comment sections — especially on finance and crypto channels — are flooded with scam comments: fake investment advice, impersonation bots, phishing links, and pump-and-dump promotions. YouTube's built-in moderation catches some, but many slip through. Manually reviewing hundreds of comments per video is not scalable.

## The Solution

Scamrem automates this workflow:

1. A creator logs in and connects their YouTube channel
2. They select a video from their channel
3. The app fetches comments via the YouTube API and sends them in batches to GPT-4o
4. GPT-4o classifies each comment as **SCAM** or **LEGIT** using a fine-tuned prompt with few-shot examples
5. The creator reviews flagged comments and removes them with a single click via the YouTube moderation API
6. Removed comments are stored in a history log and can be restored at any time

---

## Tech Stack

### Frontend

- **SvelteKit 2** — server-rendered pages, file-based routing, and server-side session validation
- **Tailwind CSS** — utility-first styling with a custom component library (Bits UI)
- **Firebase Auth** — email/password authentication with HTTP-only session cookies
- **Svelte Stores** — reactive client-side state for comments, videos, pagination, and auth
- **Axios** — API client with Bearer token authentication

### Backend

- **Flask** — REST API with CORS and custom auth middleware
- **OpenAI GPT-4o** — scam/legit classification with engineered prompts (85%+ accuracy)
- **YouTube Data API v3** — video listing, comment fetching, and comment moderation via OAuth 2.0
- **Firebase Admin SDK** — server-side token verification and Firestore database operations
- **Gunicorn** — production WSGI server (4 workers, 8 threads)
- **Docker** — containerized deployment

### Infrastructure

- **Firebase Firestore** — user profiles, OAuth tokens, and moderation history
- **Stripe** — subscription billing and plan management
- **Railway** — cloud deployment for the backend
- **Vercel / Node adapter** — frontend hosting

---

## Key Features

### AI-Powered Scam Detection

Comments are batched and analyzed by GPT-4o using a prompt engineered with few-shot examples and detection heuristics (unknown crypto tokens, fake expert recommendations, phishing patterns). Three prompt versions were tested iteratively, with the best achieving 85%+ classification accuracy.

### One-Click Moderation

Each flagged comment has **Remove** and **Approve** buttons that directly call the YouTube moderation API. No need to leave the app or navigate YouTube Studio.

### YouTube OAuth 2.0 Integration

The app handles the full OAuth 2.0 flow for YouTube's `force-ssl` scope — including token exchange, refresh token management, credential persistence in Firestore, and automatic re-authentication when tokens expire or permissions are revoked.

### Moderation History & Undo

Every removed comment is saved to a per-user Firestore subcollection with timestamps. Creators can review their moderation history and restore any comment they removed by mistake.

### Session-Based Authentication

Firebase Auth on the client exchanges ID tokens for HTTP-only session cookies on the server. Protected routes are validated server-side via Firebase Admin SDK on every request — no token leakage through JavaScript.

### Subscription Management

Stripe-backed subscription tiers gate access to the moderation dashboard. Subscription status is cached in cookies to minimize API calls, with server-side verification as a fallback.

### Responsive Dashboard

The dashboard includes video browsing, comment analysis, profile settings (email, password, channel name), and removed comment history — all with pagination, loading states, and toast notifications.

---

## Architecture Overview

```
Browser (SvelteKit)
  |
  |-- Firebase Auth (login/signup)
  |-- Session cookie <-> SvelteKit server (Firebase Admin verification)
  |-- Axios requests with Bearer token
  |
  v
Flask API (Railway / Docker)
  |
  |-- Firebase Admin SDK (token verification middleware)
  |-- YouTube Data API v3 (videos, comments, moderation)
  |-- YouTube OAuth 2.0 (per-user credentials in Firestore)
  |-- OpenAI GPT-4o (batch comment classification)
  |-- Firestore (user data, moderation history)
  |
  v
External Services
  |-- YouTube API
  |-- OpenAI API
  |-- Firebase / Firestore
  |-- Stripe (subscriptions)
```

---

## Project Structure

```
scamrem-svelte/
├── frontend/                    # SvelteKit application
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/      # Svelte components (auth, comments, videos, profile, etc.)
│   │   │   ├── server/          # Server-only code (Firebase Admin)
│   │   │   ├── stores/          # Svelte stores (auth, data, notifications)
│   │   │   ├── firebase.js      # Firebase client initialization
│   │   │   └── api.js           # API client with auth headers
│   │   ├── routes/              # SvelteKit file-based routing
│   │   │   ├── dashboard/       # Protected dashboard pages
│   │   │   ├── auth/            # Login/logout server endpoints
│   │   │   ├── login/           # Login page
│   │   │   └── privacy/         # Privacy policy
│   │   └── hooks.server.ts      # Server hooks for session validation
│   ├── .env.example             # Environment variable template
│   └── svelte.config.js
│
├── backend/                     # Flask API
│   ├── app.py                   # Flask routes and auth middleware
│   ├── viewComments.py          # YouTube API, OpenAI integration, data models
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Container configuration
│   └── .env.example             # Environment variable template
│
└── README.md
```

---

## Running Locally

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env            # fill in your API keys
# place your serviceAccountKey.json and client_secret.json in backend/
python app.py
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env            # fill in your Firebase config
npm run dev
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable                | Description                      |
| ----------------------- | -------------------------------- |
| `OPENAI_API_KEY`        | OpenAI API key for GPT-4o        |
| `YT_FO_API_KEY`         | YouTube Data API key             |
| `YT_TECH4_API_KEY`      | YouTube Data API key (secondary) |
| `RAILWAY_PUBLIC_DOMAIN` | Public domain for OAuth callback |

### Frontend (`frontend/.env`)

| Variable                              | Description                          |
| ------------------------------------- | ------------------------------------ |
| `PUBLIC_FIREBASE_API_KEY`             | Firebase client API key              |
| `PUBLIC_FIREBASE_AUTH_DOMAIN`         | Firebase auth domain                 |
| `PUBLIC_FIREBASE_PROJECT_ID`          | Firebase project ID                  |
| `PUBLIC_FIREBASE_STORAGE_BUCKET`      | Firebase storage bucket              |
| `PUBLIC_FIREBASE_MESSAGING_SENDER_ID` | Firebase messaging sender ID         |
| `PUBLIC_FIREBASE_APP_ID`              | Firebase app ID                      |
| `PUBLIC_FIREBASE_MEASUREMENT_ID`      | Firebase analytics measurement ID    |
| `FIREBASE_PROJECT_ID`                 | Firebase Admin project ID            |
| `FIREBASE_CLIENT_EMAIL`               | Firebase Admin service account email |
| `FIREBASE_PRIVATE_KEY`                | Firebase Admin private key           |

---

## What I Learned Building This

- Implementing a complete **OAuth 2.0 flow** with token persistence, refresh handling, and re-authentication fallback
- **Prompt engineering** for classification tasks — iterating through multiple prompt versions with few-shot examples to reach 85%+ accuracy
- Building a **session-based auth system** on top of Firebase using HTTP-only cookies for security
- Integrating **four external APIs** (YouTube, OpenAI, Firebase, Stripe) into a cohesive product
- Deploying a **containerized Python backend** alongside a SvelteKit frontend on separate platforms
- Handling real-world edge cases: expired tokens, revoked permissions, popup blockers, pagination across large datasets
