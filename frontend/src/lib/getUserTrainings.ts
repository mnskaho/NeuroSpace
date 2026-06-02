import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
process.env.NEXT_PUBLIC_SUPABASE_URL!,
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export async function getTrainingCount(){

const { data:{ user } } = await supabase.auth.getUser();

if(!user) return 0;

const { count } = await supabase
.from("trainings")
.select("*",{ count:"exact", head:true })
.eq("user_id",user.id);

return count || 0;

}