"use client";

import { useEffect, useMemo, useState } from "react";
import { createClient } from "@supabase/supabase-js";
import { useRouter } from "next/navigation";
import Icon from "@/components/ui/AppIcon";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

const validatePassword = (password: string) =>
  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+=[\]{};':"\\|,.<>/?~-]).{8,}$/.test(
    password
  );

export default function ResetPasswordPage() {
  const router = useRouter();
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [checkingSession, setCheckingSession] = useState(true);
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [message, setMessage] = useState<{ type: "success" | "error" | "info"; text: string } | null>(
    null
  );

  useEffect(() => {
    const establishRecoverySession = async () => {
      try {
        const url = new URL(window.location.href);
        const code = url.searchParams.get("code");
        const urlError = url.searchParams.get("error_description") || url.searchParams.get("error");

        if (urlError) throw new Error(urlError);

        if (code) {
          const { error } = await supabase.auth.exchangeCodeForSession(code);
          if (error) throw error;
          window.history.replaceState({}, document.title, window.location.pathname);
        }

        const { data, error } = await supabase.auth.getSession();
        if (error) throw error;

        if (!data.session?.user) {
          setMessage({
            type: "error",
            text: "This reset link is invalid or expired. Please request a new password reset email.",
          });
          return;
        }

        setUserEmail(data.session.user.email ?? null);
      } catch (err) {
        setMessage({
          type: "error",
          text: err instanceof Error ? err.message : "Could not validate the reset link.",
        });
      } finally {
        setCheckingSession(false);
      }
    };

    establishRecoverySession();
  }, []);

  const passwordHint = useMemo(() => {
    if (!newPassword) return "Use at least 8 characters with uppercase, lowercase, number, and symbol.";
    if (!validatePassword(newPassword)) {
      return "Password is not strong enough yet.";
    }
    if (confirmPassword && newPassword !== confirmPassword) {
      return "Passwords do not match.";
    }
    return "Password looks good.";
  }, [newPassword, confirmPassword]);

  const canSubmit =
    Boolean(userEmail) &&
    validatePassword(newPassword) &&
    newPassword === confirmPassword &&
    !loading &&
    !checkingSession;

  const handleReset = async (event: React.FormEvent) => {
    event.preventDefault();
    setMessage(null);

    if (!validatePassword(newPassword)) {
      setMessage({
        type: "error",
        text: "Password must include uppercase, lowercase, number, symbol, and at least 8 characters.",
      });
      return;
    }

    if (newPassword !== confirmPassword) {
      setMessage({ type: "error", text: "Passwords do not match." });
      return;
    }

    setLoading(true);
    try {
      const { error } = await supabase.auth.updateUser({ password: newPassword });
      if (error) throw error;

      setMessage({
        type: "success",
        text: "Your password has been updated. Redirecting to sign in...",
      });

      await supabase.auth.signOut();
      setTimeout(() => router.replace("/sign-up-login"), 1200);
    } catch (err) {
      setMessage({
        type: "error",
        text: err instanceof Error ? err.message : "Could not update your password.",
      });
    } finally {
      setLoading(false);
    }
  };

  const messageClass =
    message?.type === "success"
      ? "border-green-400/30 bg-green-500/10 text-green-300"
      : message?.type === "error"
      ? "border-red-400/30 bg-red-500/10 text-red-300"
      : "border-quantum-cyan/30 bg-quantum-cyan/10 text-quantum-cyan";

  return (
    <main className="min-h-screen quantum-grid flex items-center justify-center bg-space px-4 py-10">
      <section className="glass w-full max-w-md rounded-3xl border border-quantum-cyan/30 p-8 shadow-card">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-2xl border border-quantum-cyan/30 bg-quantum-cyan/10">
            <Icon name="LockClosedIcon" size={28} className="text-quantum-cyan" />
          </div>
          <h1 className="mb-2 font-mono text-3xl font-black text-text-primary">
            Reset Password
          </h1>
          <p className="text-sm text-text-secondary">
            Choose a new secure password for your NeuroSpace account.
          </p>
        </div>

        {checkingSession ? (
          <div className="rounded-2xl border border-quantum-purple/20 bg-panel/60 p-5 text-center">
            <p className="font-mono text-sm text-text-secondary">Checking reset link...</p>
          </div>
        ) : (
          <>
            {userEmail && (
              <div className="mb-5 rounded-2xl border border-quantum-purple/20 bg-panel/50 p-4 text-center">
                <p className="font-mono text-xs uppercase tracking-wider text-text-muted">
                  Account
                </p>
                <p className="mt-1 break-all text-sm font-semibold text-text-primary">{userEmail}</p>
              </div>
            )}

            {message && (
              <div className={`mb-5 rounded-2xl border p-4 text-sm ${messageClass}`}>
                {message.text}
              </div>
            )}

            <form onSubmit={handleReset} className="flex flex-col gap-4">
              <div>
                <label className="mb-2 block font-mono text-xs uppercase tracking-wider text-text-muted">
                  New Password
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    value={newPassword}
                    onChange={(event) => setNewPassword(event.target.value)}
                    placeholder="New password"
                    className="input-quantum w-full rounded-xl px-4 py-3 pr-12 text-sm"
                    disabled={!userEmail || loading}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted transition-colors hover:text-text-secondary"
                  >
                    <Icon name={showPassword ? "EyeSlashIcon" : "EyeIcon"} size={18} />
                  </button>
                </div>
              </div>

              <div>
                <label className="mb-2 block font-mono text-xs uppercase tracking-wider text-text-muted">
                  Confirm Password
                </label>
                <div className="relative">
                  <input
                    type={showConfirmPassword ? "text" : "password"}
                    value={confirmPassword}
                    onChange={(event) => setConfirmPassword(event.target.value)}
                    placeholder="Confirm new password"
                    className="input-quantum w-full rounded-xl px-4 py-3 pr-12 text-sm"
                    disabled={!userEmail || loading}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted transition-colors hover:text-text-secondary"
                  >
                    <Icon name={showConfirmPassword ? "EyeSlashIcon" : "EyeIcon"} size={18} />
                  </button>
                </div>
              </div>

              <p
                className={`font-mono text-xs ${
                  validatePassword(newPassword) && (!confirmPassword || newPassword === confirmPassword)
                    ? "text-quantum-cyan"
                    : "text-text-muted"
                }`}
              >
                {passwordHint}
              </p>

              <button
                type="submit"
                disabled={!canSubmit}
                className="btn-quantum mt-2 rounded-xl py-4 font-mono text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Updating..." : "Update Password"}
              </button>
            </form>

            <button
              type="button"
              onClick={() => router.replace("/sign-up-login")}
              className="mt-6 w-full rounded-xl border border-quantum-purple/20 px-4 py-3 font-mono text-xs text-text-secondary transition-colors hover:bg-panel-2 hover:text-text-primary"
            >
              Back to sign in
            </button>
          </>
        )}
      </section>
    </main>
  );
}
