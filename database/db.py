
from utils.config import SUPABASE_URL, SUPABASE_KEY
from supabase.client import create_client, Client

supabase_url = SUPABASE_URL or ""
supabase_key = SUPABASE_KEY or ""
supabase: Client = create_client(supabase_url, supabase_key)


def add_user(user_id, details):
    supabase.table('aevo_users').insert({"id": user_id, "details": details}).execute()

def get_users():
    return supabase.table('aevo_users').select("*").execute().data

def get_user(user_id):
    data = supabase.table('aevo_users').select("*").match({"id": user_id}).execute().data
    return None if len(data) == 0 else data[0]

def update_user(user_id, details):
    supabase.table('aevo_users').update({"details": details}).eq("id", user_id).execute()

def delete_user(user_id):
    supabase.table('aevo_users').delete().eq("id", user_id).execute()
