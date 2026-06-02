
"use client";

import { useState } from "react";
import { toast } from "sonner";
import {
  UserIcon,
  QuestionMarkCircleIcon,
  DocumentTextIcon,
  TrashIcon,
  ChevronLeftIcon,
  KeyIcon,
} from "@heroicons/react/24/outline";
import { useRouter } from "next/navigation";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface QuickAccessItem {
  title: string;
  subtitle: string;
  icon: React.FC<React.SVGProps<SVGSVGElement>>;
  href: string;
  bgColor: string;
}

const quickAccessItems: QuickAccessItem[] = [
  {
    title: "My Profile",
    subtitle: "Edit personal info",
    icon: UserIcon,
    href: "/profile",
    bgColor: "bg-gradient-to-tr from-blue-500 to-cyan-400 text-white",
  },
  {
    title: "Help & Support",
    subtitle: "FAQs & contact us",
    icon: QuestionMarkCircleIcon,
    href: "/help",
    bgColor: "bg-gradient-to-tr from-green-400 to-green-600 text-white",
  },
  {
    title: "Documentation",
    subtitle: "Guides & resources",
    icon: DocumentTextIcon,
    href: "/documentation",
    bgColor: "bg-gradient-to-tr from-amber-400 to-yellow-400 text-white",
  },
];

export default function SettingsPage() {
  const router = useRouter();

  /** Notifications **/
  const [emailNotifications, setEmailNotifications] = useState(true);
  /*const [productUpdates, setProductUpdates] = useState(true); */
  const [securityAlerts, setSecurityAlerts] = useState(true);
 /* const [weeklyDigest, setWeeklyDigest] = useState(false);
  const [marketing, setMarketing] = useState(false); */

  /** Privacy **/
  const [activityStatus, setActivityStatus] = useState(true);
  const [profileVisibility, setProfileVisibility] = useState("Everyone");

  /** Danger Zone **/
  const [isDeleting, setIsDeleting] = useState(false);
  const [showDeleteAlert, setShowDeleteAlert] = useState(false);

  /** Handle toggles **/
  const handleToggle = (key: string) => {
    const mapping: Record<string, [boolean, (v: boolean) => void, string]> = {
      emailNotifications: [emailNotifications, setEmailNotifications, "Email Notifications"],
     /* productUpdates: [productUpdates, setProductUpdates, "Product Updates"], */
      securityAlerts: [securityAlerts, setSecurityAlerts, "Security Alerts"],
     /* weeklyDigest: [weeklyDigest, setWeeklyDigest, "Weekly Digest"],
      marketing: [marketing, setMarketing, "Marketing Emails"], */
      activityStatus: [activityStatus, setActivityStatus, "Activity Status"],
    };
    const [state, setter, label] = mapping[key];
    setter(!state);
    toast.success(`${label} ${!state ? "enabled" : "disabled"}`);
  };

  /** Delete user via Supabase **/
  const handleDeleteAccount = async () => {
    setShowDeleteAlert(false);
    setIsDeleting(true);
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error("User not found");

      const res = await fetch("/api/delete-account", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId: user.id }),
      });

      const result = await res.json();
      if (!res.ok) throw new Error(result.error || "Failed to delete account");

      toast.success("Account deleted successfully!");
      await supabase.auth.signOut();
      router.push("/sign-up-login");

    } catch (err: any) {
      toast.error(err.message || "Something went wrong!");
    } finally {
      setIsDeleting(false);
    }
  };

  /** UI Components **/
  const Card = ({ children }: { children: React.ReactNode }) => (
    <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/50 backdrop-blur-md shadow-neon rounded-2xl p-6 space-y-4 hover:shadow-neon-xl transition-shadow duration-300">
      {children}
    </div>
  );

  const SectionTitle = ({ title }: { title: string }) => (
    <h3 className="text-lg md:text-xl font-bold text-white tracking-wide">{title}</h3>
  );

  const Switch = ({ checked, onChange }: { checked: boolean; onChange: () => void }) => (
    <button
      role="switch"
      aria-checked={checked}
      onClick={onChange}
      className={`relative inline-flex h-6 w-12 items-center rounded-full transition-all duration-300 ${
        checked ? "bg-cyan-400 shadow-neon-cyan" : "bg-gray-700"
      }`}
    >
      <span
        className={`inline-block h-5 w-5 transform rounded-full bg-white shadow-md transition-transform duration-300 ${
          checked ? "translate-x-6" : "translate-x-1"
        }`}
      />
    </button>
  );

  const Button = ({
    children,
    onClick,
    variant = "primary",
    disabled = false,
  }: {
    children: React.ReactNode;
    onClick: () => void | Promise<void>;
    variant?: "primary" | "danger" | "outline";
    disabled?: boolean;
  }) => {
    const base =
      "rounded-xl px-5 py-2 font-bold transition-all duration-200 w-fit flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed";
    const style =
      variant === "primary"
        ? "bg-gradient-to-r from-cyan-400 to-blue-500 text-white hover:shadow-neon-cyan hover:scale-105"
        : variant === "danger"
        ? "bg-gradient-to-r from-red-500 to-pink-500 text-white hover:shadow-neon-red hover:scale-105"
        : "border border-gray-600 text-white hover:bg-gray-700";

    return (
      <button className={`${base} ${style}`} onClick={onClick} disabled={disabled}>
        {children}
      </button>
    );
  };

  /** Render **/
  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6 bg-gray-900 min-h-screen relative">

      {/* BACK BUTTON */}
            <div className="sticky top-4 left-4 z-50">
        <button
          onClick={() => router.push("/dashboard")}
          className="flex items-center gap-2 text-xs font-semibold text-text-primary px-4 py-2 rounded-lg glass-cyan border border-cyan-400 transition shadow-md hover:shadow-cyan-500/60 hover:scale-105 hover:text-accent-cyan"
        >
          Back
        </button>
      </div>


      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center gap-2 md:gap-4 mb-6">
        <h1 className="text-4xl font-extrabold gradient-text-violet tracking-wider">
  Settings
</h1>
        <p className="text-gray-400">
          Manage your account, privacy, and preferences
        </p>
      </div>

      {/* Notifications */}
      <Card>
        <SectionTitle title="Notifications" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            { label: "Email Notifications", key: "emailNotifications", state: emailNotifications },
          /*  { label: "Product Updates", key: "productUpdates", state: productUpdates }, */
            { label: "Security Alerts", key: "securityAlerts", state: securityAlerts },
           /* { label: "Weekly Digest", key: "weeklyDigest", state: weeklyDigest },
            { label: "Marketing Emails", key: "marketing", state: marketing }, */
          ].map((item) => (
            <div
              key={item.key}
              className="flex justify-between items-center bg-gray-800/50 rounded-xl p-3 hover:bg-gray-800/70 transition-colors"
            >
              <span className="text-white">{item.label}</span>
              <Switch checked={item.state} onChange={() => handleToggle(item.key)} />
            </div>
          ))}
        </div>
      </Card>

      {/* Account & Security */}
      <Card>
        <SectionTitle title="Account & Security" />
        <button
          onClick={() => router.push("/profile")}
          className="w-full flex items-center justify-between bg-gray-800/50 hover:bg-gray-800/70 transition-colors rounded-xl p-4"
        >
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-xl bg-gray-700 flex items-center justify-center">
              <KeyIcon className="w-5 h-5 text-gray-300" />
            </div>
            <div className="text-left">
              <p className="font-semibold text-white">Change Password</p>
              <p className="text-sm text-gray-400">Update your account password</p>
            </div>
          </div>
          <span className="text-gray-400 text-xl">›</span>
        </button>
      </Card>

      {/* Privacy */}
      <Card>
        <SectionTitle title="Privacy" />
        <div className="flex flex-col gap-4">
          <div className="flex justify-between items-center bg-gray-800/50 p-3 rounded-xl hover:bg-gray-800/70 transition-colors">
            <span className="text-white">Activity Status</span>
            <Switch checked={activityStatus} onChange={() => handleToggle("activityStatus")} />
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-white">Profile Visibility</label>
            <select
              value={profileVisibility}
              onChange={(e) => setProfileVisibility(e.target.value)}
              className="border border-gray-600 rounded-lg p-3 w-full bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-cyan-400"
            >
              <option>Everyone</option>
              <option>Friends</option>
              <option>Only Me</option>
            </select>
          </div>
        </div>
      </Card>

      {/* Danger Zone */}
      <Card>
        <SectionTitle title="Danger Zone" />
        <p className="text-gray-400 mb-4">
          Actions here are irreversible. Proceed with caution.
        </p>
        <div className="flex gap-4 flex-wrap">
          <Button onClick={() => setShowDeleteAlert(true)} variant="danger">
            <TrashIcon className="w-5 h-5" />
            Delete Account
          </Button>
        </div>
      </Card>

      {/* Delete Confirmation Alert */}
      {showDeleteAlert && (
        <div className="absolute inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/50 backdrop-blur-md shadow-neon rounded-2xl p-6 w-full max-w-md space-y-4">
            <h3 className="text-xl font-bold text-white">Confirm Account Deletion</h3>
            <p className="text-gray-400">
              Are you sure? This action is permanent and cannot be undone.
            </p>
            <div className="flex justify-end gap-4 mt-4">
              <Button variant="outline" onClick={() => setShowDeleteAlert(false)}>Cancel</Button>
              <Button variant="danger" onClick={handleDeleteAccount} disabled={isDeleting}>
                {isDeleting ? "Deleting..." : "Delete"}
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Quick Access */}
      <Card>
        <SectionTitle title="Quick Access" />
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {quickAccessItems.map((item) => (
            <a
              key={item.title}
              href={item.href}
              className="flex items-center gap-4 p-4 rounded-2xl border border-gray-700 hover:shadow-neon-xl hover:scale-105 transition-transform duration-200"
            >
              <div
                className={`w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 ${item.bgColor} shadow-neon`}
              >
                <item.icon className="w-6 h-6" />
              </div>
              <div>
                <p className="font-bold text-white">{item.title}</p>
                <p className="text-gray-300 text-sm">{item.subtitle}</p>
              </div>
            </a>
          ))}
        </div>
      </Card>
    </div>
  );
}