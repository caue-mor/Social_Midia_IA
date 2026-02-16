import { NextRequest, NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase-server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function GET(request: NextRequest) {
  try {
    const supabase = await createServerSupabaseClient();
    const { data: { session } } = await supabase.auth.getSession();

    if (!session) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const { searchParams } = new URL(request.url);
    const platform = searchParams.get("platform") || "";
    const niche = searchParams.get("niche") || "";

    const params = new URLSearchParams();
    if (platform) params.set("platform", platform);
    if (niche) params.set("niche", niche);

    const response = await fetch(`${BACKEND_URL}/api/v1/analysis/viral?${params}`, {
      headers: {
        "Authorization": `Bearer ${session.access_token}`,
      },
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Viral content proxy error:", error);
    return NextResponse.json({ error: "Erro interno" }, { status: 500 });
  }
}
