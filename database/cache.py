
message_entry = {}

def add_message_entry(user_id, value):
    message_entry[user_id] = value

def get_message_entry(user_id):
    return message_entry.get(user_id)

trade_cache = {}

def add_trade_cache(user_id, key, value):
    trade_cache[user_id] = {**trade_cache.get(user_id, {}), key: value}

def get_trade_cache(user_id, key) -> str | None:
    return trade_cache.get(user_id, {}).get(key)

def delete_trade_cache(user_id):
    trade_cache.pop(user_id, None)

def get_trade_cache_data(user_id):
    all_data = trade_cache[user_id]
    all_data.pop('request')
    all_data.pop('asset')
    return all_data