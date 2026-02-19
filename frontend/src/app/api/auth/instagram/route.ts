import { NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase-server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function GET() {
  try {
    const supabase = await createServerSupabaseClient();
    const { data: { session } } = await supabase.auth.getSession();

    if (!session) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const response = await fetch(`${BACKEND_URL}/api/v1/auth/instagram/authorize`, {
      headers: {
        "Authorization": `Bearer ${session.access_token}`,
      },
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Instagram authorize proxy error:", error);
    return NextResponse.json({ error: "Erro interno" }, { status: 500 });
  }
}

export async function DELETE() {
  try {
    const supabase = await createServerSupabaseClient();
    const { data: { session } } = await supabase.auth.getSession();

    if (!session) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const response = await fetch(`${BACKEND_URL}/api/v1/auth/instagram/disconnect`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${session.access_token}`,
      },
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Instagram disconnect proxy error:", error);
    return NextResponse.json({ error: "Erro interno" }, { status: 500 });
  }
}
