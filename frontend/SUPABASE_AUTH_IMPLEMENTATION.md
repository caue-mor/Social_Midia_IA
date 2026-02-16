# Supabase Auth & API Routes Implementation

## Overview
Complete Supabase authentication system and API route handlers implemented for the AgenteSocial frontend.

## Files Created

### Authentication Core
1. **`/src/lib/supabase-server.ts`**
   - Server-side Supabase client with cookie handling
   - Used in middleware and API routes
   - Handles Next.js 15 async cookies API

2. **`/src/middleware.ts`**
   - Protects all routes except `/login`, `/signup`, `/auth/callback`
   - Redirects unauthenticated users to login with `redirectTo` param
   - Updates Supabase session cookies on each request

3. **`/src/components/auth/auth-provider.tsx`**
   - React Context for client-side auth state
   - Provides `user`, `loading`, `signOut` to components
   - Listens to auth state changes via `onAuthStateChange`

### Authentication Pages
4. **`/src/app/(auth)/layout.tsx`**
   - Minimal layout for auth pages (no sidebar)
   - Centered content with background styling

5. **`/src/app/(auth)/login/page.tsx`**
   - Email/password login form
   - Handles redirectTo query param
   - Client-side validation and error display

6. **`/src/app/(auth)/signup/page.tsx`**
   - User registration form
   - Password confirmation validation
   - Success state with email verification message

7. **`/src/app/auth/callback/route.ts`**
   - Handles OAuth callbacks and email confirmations
   - Exchanges code for session
   - Redirects to app after authentication

### API Route Handlers (Proxy to Backend)
8. **`/src/app/api/chat/route.ts`**
   - POST `/api/chat` - Send chat messages
   - GET `/api/chat` - List conversations
   - Proxies to `${BACKEND_URL}/api/v1/chat/*`

9. **`/src/app/api/content/route.ts`**
   - POST `/api/content` - Create content
   - GET `/api/content` - Get content library
   - Proxies to `${BACKEND_URL}/api/v1/content/*`

10. **`/src/app/api/content/generate/route.ts`**
    - POST `/api/content/generate` - Generate AI content
    - Proxies to `${BACKEND_URL}/api/v1/content/generate`

11. **`/src/app/api/analysis/profile/route.ts`**
    - POST `/api/analysis/profile` - Analyze social media profile
    - Proxies to `${BACKEND_URL}/api/v1/analysis/profile`

12. **`/src/app/api/reports/route.ts`**
    - POST `/api/reports` - Generate report
    - GET `/api/reports?type={type}` - List reports
    - Proxies to `${BACKEND_URL}/api/v1/reports/*`

13. **`/src/app/api/calendar/route.ts`**
    - POST `/api/calendar` - Create calendar event
    - GET `/api/calendar?month={month}&platform={platform}` - List events
    - Proxies to `${BACKEND_URL}/api/v1/calendar/*`

### Files Modified
14. **`/src/lib/api.ts`**
    - Added JWT token injection from Supabase session
    - Falls back to X-API-Key if no session available
    - Supports both authenticated and service calls

15. **`/src/app/layout.tsx`**
    - Wrapped app in `<AuthProvider>`
    - Provides auth context to all components

## Architecture

### Authentication Flow
```
1. User visits protected route → middleware checks auth
2. No session → redirect to /login?redirectTo={original-path}
3. User logs in → Supabase sets session cookies
4. Redirect to original path → middleware allows access
```

### API Request Flow
```
Client Component → /api/* route → Auth check → Proxy to backend with JWT
```

### Session Management
- **Client-side**: `createClient()` from `@/lib/supabase`
- **Server-side**: `createServerSupabaseClient()` from `@/lib/supabase-server`
- **Middleware**: Custom Supabase client with cookie handlers
- **API Routes**: Server client with session extraction

## Environment Variables Required

```env
# Supabase (required for auth)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# Backend API (required for proxying)
BACKEND_URL=http://localhost:8000

# Optional: Fallback API key for service calls
NEXT_PUBLIC_API_KEY=your-api-key
```

## Security Features

1. **JWT-based authentication**: All API routes extract JWT from session
2. **Authorization header**: Backend receives `Bearer {token}`
3. **Protected routes**: Middleware blocks unauthenticated access
4. **Session refresh**: Middleware updates cookies on each request
5. **Error handling**: Generic error messages (no sensitive info leaked)
6. **Public paths**: Login/signup/callback excluded from auth check

## Usage Examples

### Client Component
```tsx
"use client";
import { useAuth } from "@/components/auth/auth-provider";

export default function MyComponent() {
  const { user, loading, signOut } = useAuth();

  if (loading) return <div>Loading...</div>;
  if (!user) return null;

  return (
    <div>
      <p>Welcome {user.email}</p>
      <button onClick={signOut}>Logout</button>
    </div>
  );
}
```

### Server Component
```tsx
import { createServerSupabaseClient } from "@/lib/supabase-server";

export default async function MyServerComponent() {
  const supabase = await createServerSupabaseClient();
  const { data: { user } } = await supabase.auth.getUser();

  return <div>Server user: {user?.email}</div>;
}
```

### API Call from Frontend
```tsx
const response = await fetch("/api/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: "Hello" }),
});
```

## Testing Checklist

- [ ] Visit `/` without auth → redirects to `/login`
- [ ] Login with valid credentials → redirects to `/`
- [ ] Signup with new email → shows success message
- [ ] Confirm email → redirects to app
- [ ] Make API call to `/api/chat` → proxies to backend with JWT
- [ ] Logout → clears session and redirects to `/login`
- [ ] Visit `/login` when authenticated → should allow access (public path)

## Backend Integration

The backend must:
1. Accept `Authorization: Bearer {jwt}` header
2. Verify JWT with Supabase public key
3. Extract `user_id` from JWT claims
4. Return 401 for invalid/missing tokens

Example FastAPI middleware:
```python
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client

security = HTTPBearer()

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        user = supabase.auth.get_user(credentials.credentials)
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Next Steps

1. **Configure Supabase project**:
   - Enable Email authentication
   - Set redirect URL to `http://localhost:3000/auth/callback`
   - Customize email templates

2. **Setup backend auth**:
   - Install `@supabase/supabase-py`
   - Add JWT verification middleware
   - Extract `user_id` from token claims

3. **Add user profile**:
   - Create `profiles` table in Supabase
   - Add profile display in UI
   - Implement profile editing

4. **Enhance security**:
   - Add rate limiting
   - Implement CSRF protection
   - Add session timeout
   - Enable MFA (optional)

## Troubleshooting

### "Unauthorized" errors
- Check `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Verify session exists in browser cookies
- Check backend is accepting JWT tokens

### Infinite redirect loops
- Ensure `/login`, `/signup`, `/auth/callback` are in `publicPaths`
- Check middleware matcher excludes `/api/auth`

### API proxy errors
- Verify `BACKEND_URL` environment variable
- Check backend is running and accessible
- Look for CORS issues in backend logs

---

**Implementation Date**: February 15, 2026
**Framework**: Next.js 15 + React 19 + Supabase SSR
**Status**: Complete ✓
