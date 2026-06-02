"use client";

import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";
import { useRouter } from "next/navigation";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

const getErrorMessage = (error: unknown) => {
  if (error instanceof Error) return error.message;

  if (error && typeof error === "object") {
    const record = error as Record<string, unknown>;
    const message = record.message || record.error_description || record.details || record.hint;
    if (typeof message === "string") return message;
  }

  return "OAuth sign-in failed.";
};

export default function OAuthCallbackPage() {
  const router = useRouter();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const handleOAuth = async () => {
      try {
        const url = new URL(window.location.href);
        const code = url.searchParams.get("code");
        const oauthError = url.searchParams.get("error_description") || url.searchParams.get("error");

        if (oauthError) {
          throw new Error(oauthError);
        }

        if (code) {
          const { error } = await supabase.auth.exchangeCodeForSession(code);
          if (error) throw error;
        }

        const {
          data: { user },
          error,
        } = await supabase.auth.getUser();

        if (error) throw error;

        if (!user) {
          throw new Error("OAuth completed but no Supabase user session was found.");
        }

        const { error: profileError } = await supabase.from("profiles").upsert(
          {
            id: user.id,
            email: user.email,
            name:
              user.user_metadata?.full_name ||
              user.user_metadata?.name ||
              user.user_metadata?.user_name ||
              user.email,
            institution: user.user_metadata?.institution || null,
          },
          { onConflict: "id" }
        );
        if (profileError) throw new Error(getErrorMessage(profileError));

        router.replace("/dashboard");
      } catch (err) {
        const message = getErrorMessage(err);
        console.error("OAuth callback error:", message);
        setErrorMessage(message);
      }
    };

    handleOAuth();
  }, [router]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-space px-4">
      <div className="glass rounded-2xl border border-quantum-purple/20 p-8 text-center max-w-md">
        <p className="font-mono text-sm text-text-primary">
          {errorMessage ? "Could not connect your account." : "Connecting your account..."}
        </p>
        {errorMessage && (
          <>
            <p className="mt-3 text-xs text-red-400">{errorMessage}</p>
            <button
              onClick={() => router.replace("/sign-up-login")}
              className="btn-quantum mt-6 rounded-xl px-6 py-3 font-mono text-sm font-semibold"
            >
              Back to Sign In
            </button>
          </>
        )}
      </div>
    </div>
  );
}
