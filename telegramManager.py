import requests
import TelegramData

def send_telegram_message(message):
    """Telegram üzerinden bildirim gönder."""
    url = f"https://api.telegram.org/bot{TelegramData.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TelegramData.TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Bildirim gönderildi:", message)
    else:
        print("Bildirim gönderilemedi:", response.text)
