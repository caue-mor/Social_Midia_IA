"use client";

import { Suspense, useState, useEffect, useCallback } from "react";
import { useSearchParams } from "next/navigation";

interface SocialProfile {
  id: string;
  platform: string;
  handle: string;
  followers_count: number;
  is_active: boolean;
}

interface InstagramStatus {
  connected: boolean;
  username?: string;
  followers_count?: number;
  expires_at?: string;
  expires_in_days?: number;
}

interface BrandVoice {
  id: string;
  name: string;
  tone: string;
  vocabulary: string[];
  avoid_words: string[];
  target_audience: string;
  is_active: boolean;
}

const platformConfig: Record<string, { color: string; icon: string }> = {
  instagram: { color: "#E1306C", icon: "IG" },
  youtube: { color: "#FF0000", icon: "YT" },
  tiktok: { color: "#000000", icon: "TT" },
  linkedin: { color: "#0077B5", icon: "LI" },
};

export default function SettingsPage() {
  return (
    <Suspense fallback={<div className="p-8">Carregando...</div>}>
      <SettingsContent />
    </Suspense>
  );
}

function SettingsContent() {
  const searchParams = useSearchParams();
  const [profiles, setProfiles] = useState<SocialProfile[]>([]);
  const [instagramStatus, setInstagramStatus] = useState<InstagramStatus>({ connected: false });
  const [loadingInstagram, setLoadingInstagram] = useState(true);
  const [connectingInstagram, setConnectingInstagram] = useState(false);
  const [disconnectingInstagram, setDisconnectingInstagram] = useState(false);
  const [instagramMessage, setInstagramMessage] = useState("");
  const [brandVoice, setBrandVoice] = useState({
    name: "",
    tone: "",
    vocabulary: "",
    avoid_words: "",
    target_audience: "",
  });
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState("");
  const [newProfile, setNewProfile] = useState({ platform: "instagram", handle: "" });
  const [addingProfile, setAddingProfile] = useState(false);

  const fetchInstagramStatus = useCallback(async () => {
    try {
      const res = await fetch("/api/auth/instagram/status");
      if (res.ok) {
        const data = await res.json();
        setInstagramStatus(data);
      }
    } catch {
      // silently fail
    } finally {
      setLoadingInstagram(false);
    }
  }, []);

  useEffect(() => {
    fetchProfiles();
    fetchInstagramStatus();
  }, [fetchInstagramStatus]);

  // Handle OAuth callback query params
  useEffect(() => {
    const igParam = searchParams.get("instagram");
    if (igParam === "connected") {
      setInstagramMessage("Instagram conectado com sucesso!");
      fetchInstagramStatus();
      setTimeout(() => setInstagramMessage(""), 5000);
    } else if (igParam === "error") {
      const reason = searchParams.get("reason") || "unknown";
      setInstagramMessage(`Erro ao conectar Instagram: ${reason}`);
      setTimeout(() => setInstagramMessage(""), 5000);
    }
  }, [searchParams, fetchInstagramStatus]);

  const fetchProfiles = async () => {
    try {
      const res = await fetch("/api/settings/profiles");
      if (res.ok) {
        const data = await res.json();
        setProfiles(data.profiles || []);
      }
    } catch {
      // silently fail
    }
  };

  const addProfile = async () => {
    if (!newProfile.handle.trim()) return;
    setAddingProfile(true);
    try {
      const res = await fetch("/api/settings/profiles", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newProfile),
      });
      if (res.ok) {
        await fetchProfiles();
        setNewProfile({ platform: "instagram", handle: "" });
      }
    } catch {
      // silently fail
    } finally {
      setAddingProfile(false);
    }
  };

  const connectInstagram = async () => {
    setConnectingInstagram(true);
    try {
      const res = await fetch("/api/auth/instagram");
      if (res.ok) {
        const data = await res.json();
        if (data.authorization_url) {
          window.location.href = data.authorization_url;
          return; // Page will navigate away
        }
      }
      setInstagramMessage("Erro ao gerar URL de autorizacao. Verifique se META_APP_ID esta configurado.");
      setTimeout(() => setInstagramMessage(""), 5000);
    } catch {
      setInstagramMessage("Erro de conexao ao tentar conectar Instagram.");
      setTimeout(() => setInstagramMessage(""), 5000);
    } finally {
      setConnectingInstagram(false);
    }
  };

  const disconnectInstagram = async () => {
    if (!confirm("Deseja realmente desconectar sua conta do Instagram?")) return;
    setDisconnectingInstagram(true);
    try {
      const res = await fetch("/api/auth/instagram", { method: "DELETE" });
      if (res.ok) {
        setInstagramStatus({ connected: false });
        setInstagramMessage("Instagram desconectado.");
        await fetchProfiles();
        setTimeout(() => setInstagramMessage(""), 3000);
      }
    } catch {
      setInstagramMessage("Erro ao desconectar.");
      setTimeout(() => setInstagramMessage(""), 3000);
    } finally {
      setDisconnectingInstagram(false);
    }
  };

  const saveBrandVoice = async () => {
    setSaving(true);
    setSaveMessage("");
    try {
      const res = await fetch("/api/settings/brand-voice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: brandVoice.name || "Minha Marca",
          tone: brandVoice.tone,
          vocabulary: brandVoice.vocabulary.split(",").map((w) => w.trim()).filter(Boolean),
          avoid_words: brandVoice.avoid_words.split(",").map((w) => w.trim()).filter(Boolean),
          target_audience: brandVoice.target_audience,
        }),
      });
      setSaveMessage(res.ok ? "Salvo com sucesso!" : "Erro ao salvar.");
    } catch {
      setSaveMessage("Erro de conexao.");
    } finally {
      setSaving(false);
      setTimeout(() => setSaveMessage(""), 3000);
    }
  };

  return (
    <div className="p-8 max-w-3xl">
      <h1 className="text-2xl font-bold mb-2">Configuracoes</h1>
      <p className="text-sm text-[var(--muted-foreground)] mb-6">
        Gerencie perfis, brand voice e preferencias
      </p>

      <div className="space-y-6">
        {/* Instagram OAuth Connection */}
        <section className="p-6 rounded-lg border border-[var(--border)] bg-[var(--card)]">
          <div className="flex items-center gap-3 mb-4">
            <span
              className="w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-bold"
              style={{
                background: "linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%)",
              }}
            >
              IG
            </span>
            <div>
              <h2 className="text-lg font-semibold">Instagram</h2>
              <p className="text-xs text-[var(--muted-foreground)]">
                Conecte via OAuth para analise e publicacao
              </p>
            </div>
          </div>

          {loadingInstagram ? (
            <div className="flex items-center gap-2 text-sm text-[var(--muted-foreground)]">
              <span className="animate-spin inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full" />
              Verificando conexao...
            </div>
          ) : instagramStatus.connected ? (
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-500" />
                <span className="text-sm font-medium">
                  Conectada como @{instagramStatus.username}
                </span>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="p-3 rounded-lg bg-[var(--secondary)]">
                  <span className="block text-xs text-[var(--muted-foreground)]">Seguidores</span>
                  <span className="font-semibold">
                    {instagramStatus.followers_count?.toLocaleString() || 0}
                  </span>
                </div>
                <div className="p-3 rounded-lg bg-[var(--secondary)]">
                  <span className="block text-xs text-[var(--muted-foreground)]">Token expira em</span>
                  <span className={`font-semibold ${(instagramStatus.expires_in_days ?? 0) < 7 ? "text-red-500" : ""}`}>
                    {instagramStatus.expires_in_days != null
                      ? `${instagramStatus.expires_in_days} dias`
                      : "N/A"}
                  </span>
                </div>
              </div>
              <button
                onClick={disconnectInstagram}
                disabled={disconnectingInstagram}
                className="px-4 py-2 rounded-lg bg-red-500/10 text-red-500 text-sm hover:bg-red-500/20 transition disabled:opacity-50"
              >
                {disconnectingInstagram ? "Desconectando..." : "Desconectar Instagram"}
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-gray-400" />
                <span className="text-sm text-[var(--muted-foreground)]">Nao conectada</span>
              </div>
              <button
                onClick={connectInstagram}
                disabled={connectingInstagram}
                className="px-5 py-2.5 rounded-lg text-white text-sm font-medium transition disabled:opacity-50"
                style={{
                  background: "linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%)",
                }}
              >
                {connectingInstagram ? "Redirecionando..." : "Conectar Instagram"}
              </button>
            </div>
          )}

          {instagramMessage && (
            <p className={`mt-3 text-sm ${instagramMessage.includes("sucesso") || instagramMessage.includes("conectado") ? "text-green-600" : "text-red-500"}`}>
              {instagramMessage}
            </p>
          )}
        </section>

        <section className="p-6 rounded-lg border border-[var(--border)] bg-[var(--card)]">
          <h2 className="text-lg font-semibold mb-4">Perfis Conectados</h2>
          <p className="text-sm text-[var(--muted-foreground)] mb-4">
            Conecte suas redes sociais para analise e publicacao automatica.
          </p>

          {profiles.length > 0 && (
            <div className="space-y-2 mb-4">
              {profiles.map((profile) => (
                <div
                  key={profile.id}
                  className="flex items-center justify-between p-3 rounded-lg border border-[var(--border)]"
                >
                  <div className="flex items-center gap-3">
                    <span
                      className="w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold"
                      style={{ backgroundColor: platformConfig[profile.platform]?.color || "#666" }}
                    >
                      {platformConfig[profile.platform]?.icon || "?"}
                    </span>
                    <div>
                      <span className="text-sm font-medium">{profile.handle}</span>
                      <span className="block text-xs text-[var(--muted-foreground)]">
                        {profile.followers_count?.toLocaleString() || 0} seguidores
                      </span>
                    </div>
                  </div>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${profile.is_active ? "bg-green-500/10 text-green-600" : "bg-gray-500/10 text-gray-500"}`}>
                    {profile.is_active ? "Ativo" : "Inativo"}
                  </span>
                </div>
              ))}
            </div>
          )}

          <div className="flex gap-2">
            <select
              value={newProfile.platform}
              onChange={(e) => setNewProfile({ ...newProfile, platform: e.target.value })}
              className="px-3 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-sm"
            >
              {Object.entries(platformConfig).map(([key]) => (
                <option key={key} value={key}>{key.charAt(0).toUpperCase() + key.slice(1)}</option>
              ))}
            </select>
            <input
              value={newProfile.handle}
              onChange={(e) => setNewProfile({ ...newProfile, handle: e.target.value })}
              placeholder="@usuario"
              className="flex-1 px-4 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] text-sm"
            />
            <button
              onClick={addProfile}
              disabled={addingProfile || !newProfile.handle.trim()}
              className="px-4 py-2 rounded-lg bg-[var(--primary)] text-white text-sm disabled:opacity-50"
            >
              {addingProfile ? "..." : "Adicionar"}
            </button>
          </div>
        </section>

        <section className="p-6 rounded-lg border border-[var(--border)] bg-[var(--card)]">
          <h2 className="text-lg font-semibold mb-4">Brand Voice</h2>
          <p className="text-sm text-[var(--muted-foreground)] mb-4">
            Defina o tom de voz da sua marca para conteudos gerados pela IA.
          </p>
          <div className="space-y-3">
            <div>
              <label className="block text-xs font-medium mb-1">Nome da marca</label>
              <input
                value={brandVoice.name}
                onChange={(e) => setBrandVoice({ ...brandVoice, name: e.target.value })}
                placeholder="Ex: Minha Marca"
                className="w-full px-4 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-medium mb-1">Tom de voz</label>
              <textarea
                value={brandVoice.tone}
                onChange={(e) => setBrandVoice({ ...brandVoice, tone: e.target.value })}
                placeholder="Ex: Profissional mas acessivel, usa analogias do dia a dia para explicar conceitos complexos"
                rows={3}
                className="w-full px-4 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] text-sm"
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium mb-1">Vocabulario preferido</label>
                <input
                  value={brandVoice.vocabulary}
                  onChange={(e) => setBrandVoice({ ...brandVoice, vocabulary: e.target.value })}
                  placeholder="engajamento, estrategia, resultados"
                  className="w-full px-4 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-medium mb-1">Palavras a evitar</label>
                <input
                  value={brandVoice.avoid_words}
                  onChange={(e) => setBrandVoice({ ...brandVoice, avoid_words: e.target.value })}
                  placeholder="basicamente, literalmente"
                  className="w-full px-4 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] text-sm"
                />
              </div>
            </div>
            <div>
              <label className="block text-xs font-medium mb-1">Publico-alvo</label>
              <input
                value={brandVoice.target_audience}
                onChange={(e) => setBrandVoice({ ...brandVoice, target_audience: e.target.value })}
                placeholder="Ex: Empreendedores digitais e criadores de conteudo no Brasil"
                className="w-full px-4 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] text-sm"
              />
            </div>
          </div>
          <div className="flex items-center gap-3 mt-4">
            <button
              onClick={saveBrandVoice}
              disabled={saving}
              className="px-4 py-2 rounded-lg bg-[var(--primary)] text-white text-sm disabled:opacity-50"
            >
              {saving ? "Salvando..." : "Salvar Brand Voice"}
            </button>
            {saveMessage && (
              <span className={`text-sm ${saveMessage.includes("sucesso") ? "text-green-600" : "text-red-500"}`}>
                {saveMessage}
              </span>
            )}
          </div>
        </section>

        <section className="p-6 rounded-lg border border-[var(--border)] bg-[var(--card)]">
          <h2 className="text-lg font-semibold mb-4">API & Integracoes</h2>
          <p className="text-sm text-[var(--muted-foreground)] mb-4">
            Status das integracoes de API.
          </p>
          <div className="space-y-2">
            {[
              { name: "OpenAI", status: "Configurada", active: true },
              {
                name: "Instagram Graph API",
                status: instagramStatus.connected
                  ? `Conectada (@${instagramStatus.username})`
                  : "Nao configurada",
                active: instagramStatus.connected,
              },
              { name: "YouTube Data API", status: "Nao configurada", active: false },
              { name: "Google Trends", status: "Disponivel (sem chave)", active: true },
            ].map((api) => (
              <div key={api.name} className="flex items-center justify-between p-3 rounded-lg border border-[var(--border)]">
                <span className="text-sm">{api.name}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${api.active ? "bg-green-500/10 text-green-600" : "bg-yellow-500/10 text-yellow-600"}`}>
                  {api.status}
                </span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
