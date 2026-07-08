import { createClient } from "@supabase/supabase-js"

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL ?? "https://pwjnldzqwwagnxjycfaq.supabase.co"
const supabasePublishableKey =
  import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY ?? "sb_publishable_ILaMZuzBfV5NOnKfCQdJJQ_ESpvjbBt"

if (!supabaseUrl || !supabasePublishableKey) {
  throw new Error("Missing Supabase environment variables.")
}

export const supabase = createClient(supabaseUrl, supabasePublishableKey)
