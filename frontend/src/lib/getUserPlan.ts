import { createClient } from "@supabase/supabase-js";
import { Plan } from "./plans";

const supabase = createClient(
process.env.NEXT_PUBLIC_SUPABASE_URL!,
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export async function getUserPlan(): Promise<Plan> {

const { data:{ user } } = await supabase.auth.getUser();

if(!user) return "Free";

/* GET LAST PAYMENT */

const { data, error } = await supabase
.from("payments")
.select("plan")
.eq("user_id", user.id)
.order("created_at",{ ascending:false })
.limit(1)
.maybeSingle();

/* IF ERROR OR NO PAYMENT */

if(error || !data) return "Free";

/* RETURN PLAN */

return data.plan as Plan;

}