# API Routes Reference - AgenteSocial Frontend

## Overview
All API routes are Next.js Route Handlers that proxy requests to the FastAPI backend with JWT authentication.

## Base Configuration
- **Frontend Base**: `/api/*`
- **Backend Base**: `${BACKEND_URL}/api/v1/*` (default: `http://localhost:8000`)
- **Auth**: All routes require Supabase session, send `Authorization: Bearer {jwt}`

---

## Chat Routes

### POST `/api/chat`
Send a message to the AI chat agent.

**Frontend Call:**
```typescript
const response = await fetch("/api/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    message: "Como criar conteudo viral?",
    conversation_id: "optional-uuid"
  })
});
```

**Proxies to:** `POST ${BACKEND_URL}/api/v1/chat/`

**Response:**
```json
{
  "response": "AI generated response...",
  "conversation_id": "uuid",
  "metadata": {}
}
```

---

### GET `/api/chat`
List all conversations for the authenticated user.

**Frontend Call:**
```typescript
const response = await fetch("/api/chat");
const conversations = await response.json();
```

**Proxies to:** `GET ${BACKEND_URL}/api/v1/chat/conversations`

**Response:**
```json
[
  {
    "id": "uuid",
    "title": "Conversation title",
    "created_at": "2026-02-15T12:00:00Z",
    "updated_at": "2026-02-15T12:30:00Z",
    "message_count": 15
  }
]
```

---

## Content Routes

### GET `/api/content`
Get content library (all saved content).

**Frontend Call:**
```typescript
const response = await fetch("/api/content");
const library = await response.json();
```

**Proxies to:** `GET ${BACKEND_URL}/api/v1/content/library`

**Response:**
```json
[
  {
    "id": "uuid",
    "platform": "instagram",
    "content_type": "post",
    "text": "Caption text...",
    "media_urls": ["url1", "url2"],
    "status": "draft",
    "scheduled_at": null,
    "created_at": "2026-02-15T12:00:00Z"
  }
]
```

---

### POST `/api/content/generate`
Generate AI content for social media.

**Frontend Call:**
```typescript
const response = await fetch("/api/content/generate", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    platform: "instagram",
    content_type: "post",
    topic: "marketing digital",
    tone: "professional",
    length: "medium"
  })
});
```

**Proxies to:** `POST ${BACKEND_URL}/api/v1/content/generate`

**Request Body:**
```typescript
{
  platform: "instagram" | "tiktok" | "linkedin" | "twitter";
  content_type: "post" | "story" | "reel" | "thread";
  topic: string;
  tone?: "professional" | "casual" | "humorous" | "inspirational";
  length?: "short" | "medium" | "long";
  include_hashtags?: boolean;
  include_emojis?: boolean;
}
```

**Response:**
```json
{
  "text": "Generated caption...",
  "hashtags": ["#marketing", "#digital"],
  "suggestions": {
    "call_to_action": "Comment below!",
    "best_time": "18:00-20:00",
    "estimated_reach": "high"
  }
}
```

---

## Analysis Routes

### POST `/api/analysis/profile`
Analyze a social media profile (competitor analysis, audit).

**Frontend Call:**
```typescript
const response = await fetch("/api/analysis/profile", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    platform: "instagram",
    username: "competitor_account"
  })
});
```

**Proxies to:** `POST ${BACKEND_URL}/api/v1/analysis/profile`

**Request Body:**
```typescript
{
  platform: "instagram" | "tiktok" | "linkedin";
  username: string;
  analysis_type?: "audit" | "competitor" | "influencer";
}
```

**Response:**
```json
{
  "profile": {
    "username": "competitor_account",
    "followers": 15000,
    "following": 500,
    "posts": 320
  },
  "insights": {
    "engagement_rate": 4.2,
    "avg_likes": 630,
    "avg_comments": 45,
    "posting_frequency": "2-3 posts/week"
  },
  "content_analysis": {
    "top_performing_types": ["reels", "carousel"],
    "best_posting_times": ["18:00-20:00", "12:00-14:00"],
    "hashtag_strategy": "Mix of niche and broad hashtags"
  },
  "recommendations": [
    "Increase video content by 30%",
    "Post more consistently (daily)"
  ]
}
```

---

## Reports Routes

### GET `/api/reports?type={type}`
List all reports, optionally filtered by type.

**Frontend Call:**
```typescript
// All reports
const response = await fetch("/api/reports");

// Filtered by type
const response = await fetch("/api/reports?type=performance");
```

**Proxies to:** `GET ${BACKEND_URL}/api/v1/reports/?report_type={type}`

**Response:**
```json
[
  {
    "id": "uuid",
    "report_type": "performance",
    "title": "Monthly Performance - Jan 2026",
    "period_start": "2026-01-01",
    "period_end": "2026-01-31",
    "created_at": "2026-02-01T10:00:00Z",
    "file_url": "url-to-pdf"
  }
]
```

---

### POST `/api/reports`
Generate a new report.

**Frontend Call:**
```typescript
const response = await fetch("/api/reports", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    report_type: "performance",
    period_start: "2026-02-01",
    period_end: "2026-02-15",
    platforms: ["instagram", "tiktok"],
    include_sections: ["engagement", "reach", "growth"]
  })
});
```

**Proxies to:** `POST ${BACKEND_URL}/api/v1/reports/generate`

**Request Body:**
```typescript
{
  report_type: "performance" | "content" | "audience" | "competitor";
  period_start: string; // ISO date
  period_end: string;   // ISO date
  platforms?: string[];
  include_sections?: string[];
  format?: "pdf" | "html" | "json";
}
```

**Response:**
```json
{
  "id": "uuid",
  "status": "processing",
  "estimated_completion": "2026-02-15T13:05:00Z",
  "file_url": null
}
```

---

## Calendar Routes

### GET `/api/calendar?month={month}&platform={platform}`
Get scheduled content from the editorial calendar.

**Frontend Call:**
```typescript
// All events
const response = await fetch("/api/calendar");

// Filtered by month
const response = await fetch("/api/calendar?month=2026-02");

// Filtered by month and platform
const response = await fetch("/api/calendar?month=2026-02&platform=instagram");
```

**Proxies to:** `GET ${BACKEND_URL}/api/v1/calendar/events?month={month}&platform={platform}`

**Response:**
```json
[
  {
    "id": "uuid",
    "platform": "instagram",
    "content_type": "post",
    "scheduled_at": "2026-02-20T18:00:00Z",
    "status": "scheduled",
    "text": "Caption preview...",
    "media_count": 3,
    "created_at": "2026-02-15T12:00:00Z"
  }
]
```

---

### POST `/api/calendar`
Create a scheduled event (schedule content).

**Frontend Call:**
```typescript
const response = await fetch("/api/calendar", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    platform: "instagram",
    content_type: "post",
    scheduled_at: "2026-02-20T18:00:00Z",
    text: "Amazing content caption...",
    media_urls: ["url1", "url2"],
    hashtags: ["#marketing", "#digital"]
  })
});
```

**Proxies to:** `POST ${BACKEND_URL}/api/v1/calendar/events`

**Request Body:**
```typescript
{
  platform: "instagram" | "tiktok" | "linkedin" | "twitter";
  content_type: "post" | "story" | "reel" | "thread";
  scheduled_at: string; // ISO datetime
  text: string;
  media_urls?: string[];
  hashtags?: string[];
  location?: string;
  mention_users?: string[];
}
```

**Response:**
```json
{
  "id": "uuid",
  "status": "scheduled",
  "scheduled_at": "2026-02-20T18:00:00Z",
  "created_at": "2026-02-15T12:00:00Z"
}
```

---

## Error Handling

All routes return consistent error responses:

### 401 Unauthorized
No valid session found.
```json
{
  "error": "Unauthorized"
}
```

### 500 Internal Server Error
Backend error or connection failure.
```json
{
  "error": "Erro interno do servidor"
}
```

### Backend-specific errors
Passed through from backend with original status code.
```json
{
  "detail": "Specific error from backend",
  "code": "ERROR_CODE"
}
```

---

## Authentication Flow

1. **Client makes request** to `/api/chat` (example)
2. **Route handler** extracts Supabase session
3. **If no session**: Return `401 Unauthorized`
4. **If session exists**: Extract `access_token`
5. **Proxy to backend** with `Authorization: Bearer {access_token}`
6. **Backend validates JWT** and processes request
7. **Return response** to client with original status code

---

## Usage in Components

### Client Component (hooks pattern)
```tsx
"use client";
import { useState } from "react";

export default function ChatComponent() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();
      console.log(data.response);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input value={message} onChange={(e) => setMessage(e.target.value)} />
      <button onClick={sendMessage} disabled={loading}>
        Send
      </button>
    </div>
  );
}
```

### Server Component (direct fetch)
```tsx
import { createServerSupabaseClient } from "@/lib/supabase-server";

export default async function ContentLibrary() {
  const supabase = await createServerSupabaseClient();
  const { data: { session } } = await supabase.auth.getSession();

  if (!session) {
    return <div>Please login</div>;
  }

  // Fetch from internal API route
  const res = await fetch("http://localhost:3000/api/content", {
    headers: {
      Cookie: `sb-access-token=${session.access_token}`,
    },
  });
  const content = await res.json();

  return (
    <div>
      {content.map((item) => (
        <div key={item.id}>{item.text}</div>
      ))}
    </div>
  );
}
```

---

## Environment Variables

Required for all API routes to work:

```env
# Backend URL (required)
BACKEND_URL=http://localhost:8000

# Supabase (required for auth)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

---

**Last Updated**: February 15, 2026
**Framework**: Next.js 15 Route Handlers
**Auth**: Supabase JWT
