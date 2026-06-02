"use client";

import { useEffect, useRef, useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

import { getLatestComments, type UserComment } from "@/lib/comments";
import { supabase } from "@/lib/supabase";

const stats = [
  { label: "Datasets Analyzed", value: 1247, suffix: "+", color: "cyan" },
  { label: "QNN Models Trained", value: 3891, suffix: "+", color: "purple" },
  { label: "Avg Accuracy Gain", value: 3.4, suffix: "%", decimals: 1, color: "teal" },
  { label: "Research Papers", value: 48, suffix: "+", color: "pink" },
];

function useCounter(target: number, decimals = 0, active: boolean) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (!active) return;
    let start = 0;
    const duration = 1800;
    const step = target / (duration / 16);

    const timer = setInterval(() => {
      start += step;
      if (start >= target) {
        setCount(target);
        clearInterval(timer);
      } else {
        setCount(parseFloat(start.toFixed(decimals)));
      }
    }, 16);

    return () => clearInterval(timer);
  }, [target, decimals, active]);

  return count;
}

function StatCard({ stat, active }: { stat: (typeof stats)[0]; active: boolean }) {
  const count = useCounter(stat.value, stat.decimals ?? 0, active);
  const colorMap: Record<string, string> = {
    cyan: "text-quantum-cyan",
    purple: "text-quantum-violet",
    teal: "text-quantum-teal",
    pink: "text-quantum-pink",
  };

  return (
    <div className="glass rounded-2xl p-8 text-center metric-card border border-quantum-purple/10">
      <div
        className={`font-mono font-black mb-2 ${colorMap[stat.color]}`}
        style={{ fontSize: "clamp(2.5rem, 5vw, 4rem)" }}
      >
        {stat.decimals ? count.toFixed(stat.decimals) : Math.floor(count)}
        {stat.suffix}
      </div>
      <div className="font-mono text-xs text-text-muted uppercase tracking-widest">
        {stat.label}
      </div>
    </div>
  );
}

function getInitials(name: string) {
  const initials = name
    .split(" ")
    .map((part) => part[0])
    .filter(Boolean)
    .slice(0, 2)
    .join("")
    .toUpperCase();

  return initials || "U";
}

function formatCommentDate(value: string) {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  return date.toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  });
}

export default function StatsSection() {
  const [active, setActive] = useState(false);
  const [comments, setComments] = useState<UserComment[]>([]);
  const [commentsLoading, setCommentsLoading] = useState(true);
  const [commentsError, setCommentsError] = useState(false);
  const [commentPageStart, setCommentPageStart] = useState(0);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setActive(true);
      },
      { threshold: 0.3 }
    );

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    let isMounted = true;

    const loadComments = async () => {
      try {
        const latestComments = await getLatestComments(10);
        if (!isMounted) return;
        setComments(latestComments);
        setCommentsError(false);
      } catch {
        if (!isMounted) return;
        setCommentsError(true);
      } finally {
        if (isMounted) {
          setCommentsLoading(false);
        }
      }
    };

    loadComments();

    const channel = supabase
      .channel("homepage-user-comments")
      .on(
        "postgres_changes",
        { event: "INSERT", schema: "public", table: "user_comments" },
        (payload) => {
          const newComment = payload.new as UserComment;
          setComments((current) =>
            [newComment, ...current.filter((comment) => comment.id !== newComment.id)].slice(0, 10)
          );
          setCommentsError(false);
          setCommentsLoading(false);
        }
      )
      .subscribe();

    return () => {
      isMounted = false;
      supabase.removeChannel(channel);
    };
  }, []);

  useEffect(() => {
    if (commentPageStart >= comments.length) {
      setCommentPageStart(Math.max(0, comments.length - 3));
    }
  }, [commentPageStart, comments.length]);

  const canSlideComments = comments.length > 3;
  const visibleComments = comments.slice(commentPageStart, commentPageStart + 3);
  const isAtFirstComment = commentPageStart === 0;
  const isAtLastComment = commentPageStart + 3 >= comments.length;

  const showNextComments = () => {
    setCommentPageStart((current) => Math.min(current + 3, Math.max(0, comments.length - 3)));
  };

  const showFirstComments = () => {
    setCommentPageStart(0);
  };

  return (
    <section id="research" className="py-32 relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none quantum-grid opacity-30" />

      <div className="max-w-7xl mx-auto px-6" ref={ref}>
        <div className="mb-20">
          <span className="font-mono text-xs text-quantum-teal tracking-widest uppercase mb-4 block text-center">
            04 // Community Impact
          </span>
          <h2 className="font-mono font-black text-4xl md:text-5xl text-text-primary text-center mb-16">
            Key figures of <span className="gradient-text">research.</span>
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {stats.map((s) => (
              <StatCard key={s.label} stat={s} active={active} />
            ))}
          </div>
        </div>

        <div className="mb-8 flex flex-col gap-5 md:flex-row md:items-end md:justify-between">
          <div className="text-center md:text-left">
            <span className="font-mono text-xs text-quantum-cyan tracking-widest uppercase mb-3 block">
              Live community
            </span>
            <h3 className="font-mono font-black text-2xl md:text-3xl text-text-primary">
              Latest <span className="gradient-text">comments.</span>
            </h3>
          </div>

          {canSlideComments && !commentsError && (
            <div className="flex items-center justify-center gap-3">
              <button
                type="button"
                onClick={showFirstComments}
                disabled={isAtFirstComment}
                aria-label="Show first comments"
                className="group flex h-11 w-11 items-center justify-center rounded-full border border-quantum-purple/30 bg-white/[0.04] text-text-primary shadow-[0_0_24px_rgba(124,58,237,0.18)] transition-all hover:border-quantum-cyan/70 hover:bg-quantum-cyan/10 hover:text-quantum-cyan disabled:cursor-not-allowed disabled:opacity-35 disabled:hover:border-quantum-purple/30 disabled:hover:bg-white/[0.04] disabled:hover:text-text-primary"
              >
                <ChevronLeft className="h-5 w-5 transition-transform group-hover:-translate-x-0.5" />
              </button>

              <span className="font-mono text-[10px] uppercase tracking-widest text-text-muted">
                {Math.min(commentPageStart + 1, comments.length)}-
                {Math.min(commentPageStart + 3, comments.length)} / {comments.length}
              </span>

              <button
                type="button"
                onClick={showNextComments}
                disabled={isAtLastComment}
                aria-label="Show more comments"
                className="group flex h-11 w-11 items-center justify-center rounded-full border border-quantum-purple/30 bg-white/[0.04] text-text-primary shadow-[0_0_24px_rgba(6,182,212,0.16)] transition-all hover:border-quantum-cyan/70 hover:bg-quantum-cyan/10 hover:text-quantum-cyan disabled:cursor-not-allowed disabled:opacity-35 disabled:hover:border-quantum-purple/30 disabled:hover:bg-white/[0.04] disabled:hover:text-text-primary"
              >
                <ChevronRight className="h-5 w-5 transition-transform group-hover:translate-x-0.5" />
              </button>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {commentsLoading &&
            Array.from({ length: 3 }).map((_, index) => (
              <div
                key={`comment-skeleton-${index}`}
                className="glass rounded-2xl p-8 border border-quantum-purple/10 metric-card"
              >
                <div className="h-4 w-10 rounded bg-white/10 mb-5" />
                <div className="space-y-3 mb-6">
                  <div className="h-3 w-full rounded bg-white/10" />
                  <div className="h-3 w-5/6 rounded bg-white/10" />
                  <div className="h-3 w-2/3 rounded bg-white/10" />
                </div>
                <div className="flex items-center gap-3 pt-4 border-t border-quantum-purple/10">
                  <div className="w-10 h-10 rounded-xl bg-white/10" />
                  <div className="space-y-2">
                    <div className="h-3 w-24 rounded bg-white/10" />
                    <div className="h-2 w-16 rounded bg-white/10" />
                  </div>
                </div>
              </div>
            ))}

          {!commentsLoading && commentsError && (
            <div className="glass rounded-2xl p-8 border border-red-400/20 metric-card md:col-span-3 text-center">
              <p className="font-mono text-sm text-red-200">Unable to load comments.</p>
            </div>
          )}

          {!commentsLoading && !commentsError && comments.length === 0 && (
            <div className="glass rounded-2xl p-8 border border-quantum-purple/10 metric-card md:col-span-3 text-center">
              <p className="font-mono text-sm text-text-secondary">No comments yet.</p>
            </div>
          )}

          {!commentsLoading &&
            !commentsError &&
            visibleComments.map((comment) => (
              <div
                key={comment.id}
                className="glass rounded-2xl p-8 border border-quantum-purple/10 metric-card"
              >
                <div className="text-quantum-cyan text-2xl mb-4 font-mono">"</div>
                <p className="font-sans text-text-secondary leading-relaxed mb-6 text-sm">
                  {comment.comment}
                </p>
                <div className="flex items-center gap-3 pt-4 border-t border-quantum-purple/10">
                  <div className="w-10 h-10 rounded-xl bg-gradient-quantum flex items-center justify-center font-mono font-bold text-white text-sm flex-shrink-0">
                    {getInitials(comment.user_name)}
                  </div>
                  <div>
                    <div className="font-mono font-bold text-sm text-text-primary">
                      {comment.user_name}
                    </div>
                    <div className="font-mono text-[10px] text-text-muted">
                      {formatCommentDate(comment.created_at)}
                    </div>
                  </div>
                </div>
              </div>
            ))}
        </div>

        <div
          id="final-cta"
          className="mt-20 glass rounded-3xl p-12 text-center neon-border relative overflow-hidden"
        >
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              background:
                "radial-gradient(ellipse at center, rgba(124,58,237,0.08) 0%, transparent 70%)",
            }}
          />

          <h2 className="font-mono font-black text-3xl md:text-5xl text-text-primary mb-4 relative z-10">
            Ready to explore <span className="gradient-text">quantum advantage</span> ?
          </h2>

          <p className="font-sans text-text-secondary text-lg max-w-xl mx-auto mb-8 relative z-10">
            Join the researchers who use NeuroSpace to push the boundaries of quantum machine
            learning.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 relative z-10">
            <a
              href="/documentation"
              className="btn-quantum px-10 py-4 rounded-xl text-sm font-mono font-semibold"
            >
              <span>Explore more -&gt;</span>
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
