"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const router = useRouter();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("As senhas nao coincidem.");
      return;
    }

    if (password.length < 6) {
      setError("A senha deve ter pelo menos 6 caracteres.");
      return;
    }

    setLoading(true);

    const supabase = createClient();
    const { error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      setError(error.message);
      setLoading(false);
      return;
    }

    setSuccess(true);
    setLoading(false);
  };

  if (success) {
    return (
      <div className="w-full max-w-sm p-8 rounded-xl border border-[var(--border)] bg-[var(--card)] text-center">
        <h1 className="text-2xl font-bold mb-2">Conta criada!</h1>
        <p className="text-sm text-[var(--muted-foreground)] mb-4">
          Verifique seu email para confirmar a conta.
        </p>
        <Link
          href="/login"
          className="inline-block px-4 py-2 rounded-lg bg-[var(--primary)] text-white text-sm"
        >
          Ir para Login
        </Link>
      </div>
    );
  }

  return (
    <div className="w-full max-w-sm p-8 rounded-xl border border-[var(--border)] bg-[var(--card)]">
      <div className="text-center mb-6">
        <h1 className="text-2xl font-bold">AgenteSocial</h1>
        <p className="text-sm text-[var(--muted-foreground)] mt-1">
          Crie sua conta
        </p>
      </div>

      <form onSubmit={handleSignup} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-4 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
            placeholder="seu@email.com"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Senha</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full px-4 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
            placeholder="••••••••"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Confirmar Senha</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            className="w-full px-4 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
            placeholder="••••••••"
          />
        </div>

        {error && (
          <p className="text-sm text-red-500">{error}</p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full py-2 rounded-lg bg-[var(--primary)] text-white font-medium disabled:opacity-50 hover:opacity-90 transition-opacity"
        >
          {loading ? "Criando..." : "Criar Conta"}
        </button>
      </form>

      <p className="text-sm text-center mt-4 text-[var(--muted-foreground)]">
        Ja tem conta?{" "}
        <Link href="/login" className="text-[var(--primary)] hover:underline">
          Entrar
        </Link>
      </p>
    </div>
  );
}
