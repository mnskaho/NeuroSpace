export const PLAN_LIMITS = {
Free: 1,
Pro: 10,
Enterprise: Infinity
} as const;

export type Plan = keyof typeof PLAN_LIMITS;