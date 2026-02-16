import { createClient } from "./supabase";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface FetchOptions extends RequestInit {
  json?: unknown;
}

export async function api(path: string, options: FetchOptions = {}) {
  const { json, headers: customHeaders, ...rest } = options;

  const headers: Record<string, string> = {
    ...(customHeaders as Record<string, string>),
  };

  if (json) {
    headers["Content-Type"] = "application/json";
  }

  // Add JWT from Supabase session
  try {
    const supabase = createClient();
    const { data: { session } } = await supabase.auth.getSession();
    if (session?.access_token) {
      headers["Authorization"] = `Bearer ${session.access_token}`;
    }
  } catch {
    // No session available
  }

  // Fallback API key for service calls
  const apiKey = process.env.NEXT_PUBLIC_API_KEY || "";
  if (apiKey && !headers["Authorization"]) {
    headers["X-API-Key"] = apiKey;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...rest,
    headers,
    body: json ? JSON.stringify(json) : rest.body,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }

  return response.json();
}
