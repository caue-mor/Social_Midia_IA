# Authentication & API Deployment Checklist

## Pre-Deployment Setup

### 1. Supabase Project Configuration

- [ ] Create Supabase project at https://supabase.com
- [ ] Copy `SUPABASE_URL` and `SUPABASE_ANON_KEY` from project settings
- [ ] Enable Email authentication in Auth settings
- [ ] Configure email templates (optional but recommended)
- [ ] Set Site URL to production domain (e.g., `https://agentesocial.com`)
- [ ] Add redirect URLs:
  - [ ] `http://localhost:3000/auth/callback` (development)
  - [ ] `https://agentesocial.com/auth/callback` (production)
- [ ] Configure email provider (SMTP or Supabase default)
- [ ] Test email delivery with test signup

### 2. Environment Variables

Create `.env.local` file in frontend root:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Backend API
BACKEND_URL=http://localhost:8000

# Optional: API Key for service calls
NEXT_PUBLIC_API_KEY=your-service-api-key
```

**Production `.env.production`:**
```env
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
BACKEND_URL=https://api.agentesocial.com
NEXT_PUBLIC_API_KEY=production-api-key
```

### 3. Backend Integration

- [ ] Install Supabase library in backend: `pip install supabase`
- [ ] Add JWT verification middleware (see example below)
- [ ] Update CORS to allow frontend domain
- [ ] Add `Authorization` header parsing
- [ ] Extract `user_id` from JWT claims
- [ ] Test with Postman/curl using real JWT

**Example FastAPI middleware:**
```python
from fastapi import Security, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
import os

security = HTTPBearer()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    supabase: Client = Depends(get_supabase)
):
    try:
        user = supabase.auth.get_user(credentials.credentials)
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication")

# Use in routes
@app.get("/api/v1/chat/conversations")
async def get_conversations(user = Depends(get_current_user)):
    user_id = user.id
    # Query conversations for this user_id
    ...
```

---

## Local Development Testing

### 4. Authentication Flow Testing

- [ ] Start frontend: `npm run dev`
- [ ] Start backend: `uvicorn main:app --reload --port 8000`
- [ ] Visit `http://localhost:3000`
- [ ] Should redirect to `/login` (unauthenticated)
- [ ] Click "Criar conta" link
- [ ] Signup with test email
- [ ] Verify email confirmation page shows
- [ ] Check inbox for confirmation email
- [ ] Click confirmation link in email
- [ ] Should redirect to app homepage
- [ ] Verify session cookie exists in DevTools
- [ ] Test logout button (should clear session and redirect to login)
- [ ] Login again with same credentials
- [ ] Should redirect to homepage after login

### 5. API Routes Testing

Test each API route with authenticated session:

**Chat Routes:**
- [ ] POST `/api/chat` - Send test message
- [ ] GET `/api/chat` - List conversations
- [ ] Verify JWT in `Authorization` header
- [ ] Check backend receives user_id from JWT

**Content Routes:**
- [ ] GET `/api/content` - Get content library
- [ ] POST `/api/content/generate` - Generate content
- [ ] Verify AI response returns

**Analysis Routes:**
- [ ] POST `/api/analysis/profile` - Analyze profile
- [ ] Check analysis results format

**Reports Routes:**
- [ ] GET `/api/reports` - List reports
- [ ] POST `/api/reports` - Generate report
- [ ] Check report processing status

**Calendar Routes:**
- [ ] GET `/api/calendar` - Get events
- [ ] POST `/api/calendar` - Schedule content
- [ ] Verify scheduled time format

### 6. Error Handling Testing

- [ ] Test with invalid JWT (should return 401)
- [ ] Test with expired session (should redirect to login)
- [ ] Test with backend down (should return 500)
- [ ] Test with malformed request body (should return 4xx)
- [ ] Verify error messages don't leak sensitive info

### 7. Security Testing

- [ ] Verify middleware blocks unauthenticated access
- [ ] Test public paths bypass auth (login, signup, callback)
- [ ] Check JWT is not exposed in client-side logs
- [ ] Verify session cookies are HttpOnly (check DevTools)
- [ ] Test CORS from unauthorized domain (should fail)
- [ ] Check API routes reject requests without session

---

## Production Deployment

### 8. Frontend Deployment (Vercel/Netlify)

**Vercel:**
- [ ] Connect GitHub repo
- [ ] Set environment variables in Vercel dashboard
- [ ] Set `BACKEND_URL` to production API
- [ ] Deploy and test
- [ ] Verify auth flow on production domain

**Netlify:**
- [ ] Connect GitHub repo
- [ ] Set environment variables in Netlify dashboard
- [ ] Add `_redirects` file for SPA routing:
  ```
  /* /index.html 200
  ```
- [ ] Deploy and test

### 9. Backend Deployment (Railway/Render)

- [ ] Deploy FastAPI backend
- [ ] Set `SUPABASE_URL` and `SUPABASE_ANON_KEY` env vars
- [ ] Update `BACKEND_URL` in frontend to production API
- [ ] Enable CORS for production frontend domain
- [ ] Test health endpoint: `https://api.agentesocial.com/health`

### 10. Supabase Production Config

- [ ] Update Site URL to production domain
- [ ] Add production redirect URL
- [ ] Test email delivery in production
- [ ] Enable rate limiting (optional)
- [ ] Configure session timeout (default: 1 hour)
- [ ] Setup database backups
- [ ] Enable Supabase Auth logging

### 11. Domain & SSL

- [ ] Configure custom domain
- [ ] Verify SSL certificate
- [ ] Test HTTPS redirect
- [ ] Update redirect URLs in Supabase to use HTTPS

---

## Post-Deployment Verification

### 12. Production Smoke Tests

- [ ] Visit production URL
- [ ] Signup with real email
- [ ] Confirm email
- [ ] Login
- [ ] Test chat functionality
- [ ] Test content generation
- [ ] Test profile analysis
- [ ] Test report generation
- [ ] Test calendar scheduling
- [ ] Logout and login again

### 13. Performance Testing

- [ ] Check Lighthouse score (target: >90)
- [ ] Test API response times (target: <500ms)
- [ ] Monitor backend logs for errors
- [ ] Check Supabase Auth dashboard for sessions
- [ ] Verify no memory leaks in DevTools

### 14. Monitoring Setup

- [ ] Setup Vercel Analytics (frontend)
- [ ] Setup Sentry or similar (error tracking)
- [ ] Monitor Supabase Auth logs
- [ ] Setup uptime monitoring (UptimeRobot)
- [ ] Configure alerts for 5xx errors

---

## Troubleshooting Guide

### Issue: Infinite redirect loop
**Cause:** Middleware not excluding public paths
**Fix:** Check `publicPaths` array in middleware.ts includes `/login`, `/signup`, `/auth/callback`

### Issue: 401 Unauthorized on API calls
**Cause:** Session not being passed or JWT expired
**Fix:**
1. Check session exists in browser cookies
2. Verify `NEXT_PUBLIC_SUPABASE_URL` is set
3. Test session refresh by reloading page
4. Check backend JWT verification logic

### Issue: Email confirmation not working
**Cause:** Redirect URL not whitelisted
**Fix:** Add callback URL to Supabase Auth settings

### Issue: Backend not receiving user_id
**Cause:** JWT not being parsed correctly
**Fix:**
1. Verify backend extracts token from `Authorization: Bearer {token}`
2. Use Supabase client to parse JWT: `supabase.auth.get_user(token)`
3. Check JWT is valid (not expired)

### Issue: CORS errors
**Cause:** Backend not allowing frontend domain
**Fix:** Add frontend domain to CORS allowed origins in backend

### Issue: Session expires too quickly
**Cause:** Default session timeout
**Fix:** Configure session timeout in Supabase Auth settings (max: 1 week)

---

## Security Best Practices

- [ ] Never commit `.env` files to Git
- [ ] Use different Supabase projects for dev/staging/prod
- [ ] Rotate API keys regularly
- [ ] Enable MFA for admin accounts
- [ ] Implement rate limiting on API routes
- [ ] Log authentication attempts
- [ ] Monitor for suspicious activity
- [ ] Use Supabase RLS for database security
- [ ] Implement CSRF protection (Next.js handles this)
- [ ] Keep dependencies updated (`npm audit`)

---

## Rollback Plan

If issues occur in production:

1. **Immediate rollback:**
   - [ ] Revert to previous Vercel deployment
   - [ ] Check if backend needs rollback too

2. **Database rollback:**
   - [ ] Supabase has automatic backups (restore if needed)
   - [ ] Check Supabase dashboard for point-in-time recovery

3. **Hotfix process:**
   - [ ] Fix locally
   - [ ] Test thoroughly
   - [ ] Deploy to staging first
   - [ ] Deploy to production

---

## Success Metrics

After deployment, monitor:

- **Auth metrics:**
  - [ ] Signup conversion rate >70%
  - [ ] Email confirmation rate >80%
  - [ ] Login success rate >95%
  - [ ] Session duration avg >15 minutes

- **API metrics:**
  - [ ] API success rate >99%
  - [ ] Average response time <500ms
  - [ ] Zero auth-related errors

- **Performance:**
  - [ ] Lighthouse score >90
  - [ ] First Contentful Paint <1.5s
  - [ ] Time to Interactive <3s

---

**Checklist Version**: 1.0
**Last Updated**: February 15, 2026
**Responsible**: DevOps Team
