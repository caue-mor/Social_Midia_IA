# Quick Start Guide - AgenteSocial Auth Setup

## Prerequisites
- Node.js 18+ installed
- Supabase account (free tier is fine)
- Backend running on port 8000

---

## 5-Minute Setup

### Step 1: Create Supabase Project (2 minutes)

1. Go to https://supabase.com/dashboard
2. Click "New Project"
3. Fill in:
   - **Name**: AgenteSocial
   - **Database Password**: (generate strong password)
   - **Region**: Choose closest to you
4. Wait for project creation (~1 minute)
5. Go to **Settings** → **API**
6. Copy these values:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key** (starts with `eyJhbGci...`)

### Step 2: Enable Email Auth (30 seconds)

1. Go to **Authentication** → **Providers**
2. Find **Email** provider
3. Enable it if not already enabled
4. Click **Save**

### Step 3: Configure Redirect URLs (30 seconds)

1. Go to **Authentication** → **URL Configuration**
2. Add to **Redirect URLs**:
   ```
   http://localhost:3000/auth/callback
   ```
3. Set **Site URL** to:
   ```
   http://localhost:3000
   ```
4. Click **Save**

### Step 4: Setup Environment Variables (1 minute)

Create `/Users/steveherison/AgenteSocial/frontend/.env.local`:

```env
# Supabase (replace with YOUR values from Step 1)
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Backend API
BACKEND_URL=http://localhost:8000

# Optional: API Key for service calls
NEXT_PUBLIC_API_KEY=your-api-key-here
```

**Important**: Replace `xxxxx` and the anon key with your actual values!

### Step 5: Start Development Server (30 seconds)

```bash
cd /Users/steveherison/AgenteSocial/frontend
npm run dev
```

### Step 6: Test Authentication (1 minute)

1. Open http://localhost:3000 in browser
2. You should be redirected to `/login`
3. Click "Criar conta"
4. Fill in:
   - Email: your@email.com
   - Password: (at least 6 characters)
   - Confirm Password: (same)
5. Click "Criar Conta"
6. See success message
7. Check your email for confirmation link
8. Click link in email
9. You'll be redirected to the app
10. You're logged in! 🎉

---

## Test API Routes

Once logged in, open browser DevTools (F12) and run in Console:

```javascript
// Test chat API
fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'Hello AI!' })
}).then(r => r.json()).then(console.log);

// Test content generation
fetch('/api/content/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    platform: 'instagram',
    topic: 'marketing digital',
    content_type: 'post'
  })
}).then(r => r.json()).then(console.log);
```

You should see responses in the console!

---

## Troubleshooting

### "Failed to fetch" error
**Problem**: Backend not running
**Solution**: Start backend with `uvicorn main:app --reload --port 8000`

### "Unauthorized" error
**Problem**: No session or expired
**Solution**:
1. Logout and login again
2. Check cookies in DevTools → Application → Cookies
3. Should see `sb-access-token` and `sb-refresh-token`

### Email not received
**Problem**: Supabase default email has delays
**Solution**:
1. Wait 5 minutes (Supabase emails can be slow)
2. Check spam folder
3. Try with Gmail (other providers may block)

### Infinite redirect loop
**Problem**: Middleware configuration issue
**Solution**: Check `/src/middleware.ts` has correct public paths

### "CORS error"
**Problem**: Backend not allowing frontend domain
**Solution**: Add to backend CORS origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Development Workflow

### Daily Development
```bash
# Terminal 1: Frontend
cd frontend
npm run dev

# Terminal 2: Backend
cd backend
uvicorn main:app --reload --port 8000
```

### Test Changes
1. Make code changes
2. Save file (Next.js auto-reloads)
3. Refresh browser
4. Check console for errors

### Check Auth Status
Add to any component:
```tsx
import { useAuth } from "@/components/auth/auth-provider";

export default function MyComponent() {
  const { user, loading } = useAuth();
  console.log("User:", user?.email);
  console.log("Loading:", loading);
  return <div>Check console</div>;
}
```

---

## Production Deployment

See `AUTH_DEPLOYMENT_CHECKLIST.md` for complete guide.

### Quick Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd /Users/steveherison/AgenteSocial/frontend
vercel

# Follow prompts, add environment variables when asked
```

Add these environment variables in Vercel dashboard:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `BACKEND_URL` (production backend URL)

---

## Useful Commands

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Type checking
npx tsc --noEmit

# Lint code
npm run lint
```

---

## File Locations

Quick reference for editing:

- **Login page**: `src/app/(auth)/login/page.tsx`
- **Signup page**: `src/app/(auth)/signup/page.tsx`
- **Middleware**: `src/middleware.ts`
- **Auth provider**: `src/components/auth/auth-provider.tsx`
- **API routes**: `src/app/api/*/route.ts`
- **Environment**: `.env.local` (create this!)

---

## Next Steps

1. **Customize UI**: Edit login/signup pages styling
2. **Add OAuth**: Enable Google/GitHub in Supabase
3. **User Profiles**: Create profiles table in Supabase
4. **Error Handling**: Add toast notifications
5. **Loading States**: Improve UX with skeletons
6. **Protected Routes**: Add role-based access
7. **Session Timeout**: Configure in Supabase settings

---

## Support

- **Docs**: See `SUPABASE_AUTH_IMPLEMENTATION.md`
- **API Ref**: See `API_ROUTES_REFERENCE.md`
- **Deploy**: See `AUTH_DEPLOYMENT_CHECKLIST.md`
- **Summary**: See `IMPLEMENTATION_SUMMARY.md`

---

## Success Checklist

After setup, you should be able to:

- [x] Visit app and see login page
- [x] Create new account
- [x] Receive confirmation email
- [x] Login with credentials
- [x] See dashboard after login
- [x] Make API calls from DevTools
- [x] Logout successfully

---

**Setup Time**: ~5 minutes
**Status**: Ready to use ✓
**Last Updated**: February 15, 2026
