export interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
}

export interface Conversation {
  id: string;
  title: string;
  agent_type: string;
  messages: Message[];
  created_at: string;
  updated_at: string;
}

export interface ContentPiece {
  id: string;
  content_type: string;
  platform: string;
  title?: string;
  body: string;
  hashtags: string[];
  caption?: string;
  tone?: string;
  status: string;
  created_at: string;
}

export interface SocialProfile {
  id: string;
  platform: string;
  handle: string;
  followers_count: number;
  is_active: boolean;
}

export interface CalendarEvent {
  id: string;
  title: string;
  content_id?: string;
  platform: string;
  scheduled_at: string;
  status: string;
}

export interface ViralContent {
  id: string;
  platform: string;
  author_handle: string;
  content_text: string;
  virality_score: number;
  classification: string;
  niche: string;
}

export interface Report {
  id: string;
  type: string;
  period_start: string;
  period_end: string;
  data: Record<string, unknown>;
  pdf_url?: string;
}
