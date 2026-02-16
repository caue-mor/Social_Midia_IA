# Component Decomposition - AgenteSocial Frontend

## Overview
Extracted reusable components from monolithic page files to improve maintainability, reusability, and testability.

## Created Components

### Chat Components (`src/components/chat/`)

#### 1. ChatMessage (`chat-message.tsx`)
- Displays individual chat messages with role-based styling
- Supports markdown rendering for assistant responses
- Props: `role`, `content`
- Features:
  - User messages: right-aligned, primary color background
  - Assistant messages: left-aligned, secondary background, markdown support

#### 2. ChatInput (`chat-input.tsx`)
- Input field with send button and optional suggestions
- Props: `onSend`, `loading`, `suggestions`
- Features:
  - Auto-focus when not loading
  - Enter key to send
  - Suggestion chips (displayed when input is empty)
  - Disabled state during loading

### Dashboard Components (`src/components/dashboard/`)

#### 3. StatsCard (`stats-card.tsx`)
- Reusable statistics card with optional trend indicator
- Props: `title`, `value`, `description`, `trend`, `trendValue`
- Features:
  - Color-coded trend indicators (up/down/neutral)
  - Flexible value type (string or number)
  - Optional description text

### Content Components (`src/components/content/`)

#### 4. ContentCard (`content-card.tsx`)
- Displays content items with platform and status badges
- Props: `title`, `body`, `platform`, `contentType`, `status`, `createdAt`, `onEdit`
- Features:
  - Platform-specific color coding (Instagram, YouTube, TikTok, LinkedIn)
  - Status badges (draft, scheduled, published, archived)
  - Line-clamp for body text (max 3 lines)
  - Optional edit button
  - Formatted date display

### Calendar Components (`src/components/calendar/`)

#### 5. EventCard (`event-card.tsx`)
- Compact event card for calendar grid
- Props: `title`, `platform`, `scheduledAt`, `status`, `onEdit`
- Features:
  - Time display in PT-BR format
  - Platform label
  - Click handler for editing
  - Hover effects

## Custom Hooks

### useChat (`src/hooks/use-chat.ts`)
- Encapsulates chat logic and state management
- Options: `apiUrl` (default: `/api/chat`)
- Returns: `messages`, `loading`, `error`, `sendMessage`, `clearMessages`
- Features:
  - Automatic message state updates
  - Error handling with user-friendly messages
  - Loading state management
  - Clear messages utility

## Refactored Pages

### 1. Chat Page (`src/app/chat/page.tsx`)
**Before:** 136 lines with inline state management and UI components
**After:** 68 lines using extracted components and custom hook

**Changes:**
- Uses `useChat` hook for state management
- Uses `ChatMessage` component for message rendering
- Uses `ChatInput` component for input UI
- Moved suggestions to page-level constant
- Reduced code by ~50%

### 2. Dashboard Page (`src/app/page.tsx`)
**Before:** Basic grid with hardcoded cards
**After:** Enhanced with stats cards

**Changes:**
- Added `StatsCard` components for metrics display
- 4-column responsive grid for stats
- Placeholder data ready for backend integration

### 3. Sidebar (`src/components/layout/sidebar.tsx`)
**Before:** Basic navigation without user info
**After:** Enhanced with auth integration

**Changes:**
- Integrated `useAuth` hook
- Displays user email when authenticated
- Sign out button
- Maintains all existing navigation logic

## Benefits

1. **Reusability**: Components can be used across multiple pages
2. **Maintainability**: Single source of truth for each component
3. **Testability**: Isolated components easier to unit test
4. **Consistency**: Shared components ensure consistent UI/UX
5. **Code Reduction**: Removed ~100 lines of duplicate code
6. **Type Safety**: All components fully typed with TypeScript

## Next Steps

### Potential Additional Components
- `ContentForm` - for creating/editing content
- `CalendarGrid` - full calendar view component
- `AnalyticsChart` - chart wrapper with loading states
- `FilterBar` - shared filtering UI
- `EmptyState` - consistent empty state messaging
- `LoadingSpinner` - reusable loading indicator

### Hooks to Create
- `useContent` - content CRUD operations
- `useCalendar` - calendar data management
- `useAnalytics` - analytics data fetching
- `useProfiles` - social media profile management

### Performance Optimizations
- Add React.memo to pure components
- Implement virtualization for long lists
- Add suspense boundaries for code splitting
- Optimize re-renders with useCallback/useMemo

## File Structure

```
frontend/src/
├── components/
│   ├── chat/
│   │   ├── chat-message.tsx
│   │   └── chat-input.tsx
│   ├── dashboard/
│   │   └── stats-card.tsx
│   ├── content/
│   │   └── content-card.tsx
│   ├── calendar/
│   │   └── event-card.tsx
│   ├── layout/
│   │   └── sidebar.tsx (updated)
│   └── auth/
│       └── auth-provider.tsx (existing)
├── hooks/
│   └── use-chat.ts
└── app/
    ├── page.tsx (updated)
    └── chat/
        └── page.tsx (updated)
```

## Usage Examples

### ChatMessage
```tsx
<ChatMessage
  role="user"
  content="Hello, how are you?"
/>
```

### ChatInput
```tsx
<ChatInput
  onSend={(msg) => console.log(msg)}
  loading={false}
  suggestions={["Suggestion 1", "Suggestion 2"]}
/>
```

### StatsCard
```tsx
<StatsCard
  title="Total Views"
  value="1.2K"
  trend="up"
  trendValue="+15%"
  description="from last month"
/>
```

### ContentCard
```tsx
<ContentCard
  title="Marketing Post"
  body="Check out our latest product..."
  platform="instagram"
  contentType="post"
  status="scheduled"
  createdAt="2025-02-15T10:00:00Z"
  onEdit={() => router.push('/content/123')}
/>
```

### EventCard
```tsx
<EventCard
  title="Product Launch"
  platform="instagram"
  scheduledAt="2025-02-20T14:00:00Z"
  status="scheduled"
  onEdit={() => openEditModal()}
/>
```

### useChat Hook
```tsx
const { messages, loading, sendMessage } = useChat({
  apiUrl: '/api/custom-chat'
});

// Send a message
sendMessage("What's the weather today?");
```
