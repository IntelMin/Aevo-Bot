
import requests
from .config import BOT_TOKEN

def send_telegram_alert(chat_id: str, text: str, parse_mode: str = "Markdown", reply_markup: str = None):
    base_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup
    }
    response = requests.get(base_url, params=payload)
    return response.json()