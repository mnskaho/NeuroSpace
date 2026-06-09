export const PLAN_LIMITS = {
Free: 1,
Pro: 5,
"Pro+": 25
} as const;

export type Plan = keyof typeof PLAN_LIMITS;
