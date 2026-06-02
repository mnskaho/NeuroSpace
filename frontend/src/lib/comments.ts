import type { User } from "@supabase/supabase-js";

import { supabase } from "@/lib/supabase";

export type UserComment = {
  id: string;
  user_id: string;
  user_name: string;
  comment: string;
  source: string;
  created_at: string;
};

type ProfileRecord = Partial<Record<string, unknown>>;

const readString = (record: ProfileRecord | null | undefined, key: string) => {
  const value = record?.[key];
  return typeof value === "string" ? value.trim() : "";
};

export async function getLatestComments(limit = 10): Promise<UserComment[]> {
  const { data, error } = await supabase
    .from("user_comments")
    .select("id,user_id,user_name,comment,source,created_at")
    .order("created_at", { ascending: false })
    .limit(limit);

  if (error) {
    throw error;
  }

  return (data ?? []) as UserComment[];
}

export async function getCurrentProfileDisplayName(user: User): Promise<string> {
  const { data } = await supabase
    .from("profiles")
    .select("*")
    .eq("id", user.id)
    .maybeSingle();

  const profile = data as ProfileRecord | null;
  const fullName = readString(profile, "full_name");
  const username = readString(profile, "username");
  const name = readString(profile, "name");

  return fullName || username || name || user.email || "User";
}

export async function submitUserComment(comment: string): Promise<UserComment> {
  const cleanedComment = comment.trim();

  if (!cleanedComment) {
    throw new Error("Comment cannot be empty.");
  }

  const {
    data: { user },
    error: userError,
  } = await supabase.auth.getUser();

  if (userError || !user) {
    throw new Error("Please sign in to submit a comment.");
  }

  const userName = await getCurrentProfileDisplayName(user);

  const { data, error } = await supabase
    .from("user_comments")
    .insert({
      user_id: user.id,
      user_name: userName,
      comment: cleanedComment,
      source: "visualization",
    })
    .select("id,user_id,user_name,comment,source,created_at")
    .single();

  if (error) {
    throw error;
  }

  return data as UserComment;
}
