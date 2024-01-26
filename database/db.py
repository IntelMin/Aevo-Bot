import json
from utils.config import SUPABASE_URL, SUPABASE_KEY
from utils.hash import encrypt, decrypt
from supabase.client import create_client, Client
from typing import Union

supabase_url = SUPABASE_URL or ""
supabase_key = SUPABASE_KEY or ""
supabase: Client = create_client(supabase_url, supabase_key)


def add_user(user_id: int, details: dict) -> None:
    _detail = json.dumps(details)
    detail = encrypt(_detail)
    supabase.table('aevo_users').insert({"id": user_id, "details": detail}).execute()

def get_user(user_id: int) -> Union[dict, None]:
    data = supabase.table('aevo_users').select("*").match({"id": user_id}).execute().data
    if len(data) == 0:
        return None
    data = decrypt(data[0]["details"])
    return json.loads(data)

def update_user(user_id, details):
    supabase.table('aevo_users').update({"details": details}).eq("id", user_id).execute()

def delete_user(user_id):
    supabase.table('aevo_users').delete().eq("id", user_id).execute()

