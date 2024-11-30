import requests
import TelegramData
import time
import ZaraChecker
from datetime import datetime

OFFSET = 0  # Daha önce işlenmiş mesajları tekrar almamak için kullanılır

size_mapping = {
    "xs": "XS (US XS)",
    "s": "S (US S)",
    "m": "M (US M)",
    "l": "L (US L)",
    "xl": "XL (US XL)"
}

# Define the bot's start date
bot_start_date = datetime(2023, 10, 1)  # Example start date

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TelegramData.TELEGRAM_BOT_TOKEN}/sendMessage"
    """Telegram üzerinden bildirim gönder."""
    payload = {
        "chat_id": TelegramData.TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Bildirim gönderildi:", message)
    else:
        print("Bildirim gönderilemedi:", response.text)

def send_inits():
    send_telegram_message("url: ürün linki yazınız.")
    send_telegram_message("beden: ürün bedenini yazınız.(xs,s,m,l,xl)")

def listen_to_user():
    bot_start_date = datetime.now()
    telegramurl = f"https://api.telegram.org/bot{TelegramData.TELEGRAM_BOT_TOKEN}"
    send_telegram_message("Bot başlatılıyor...")
    send_inits()

    global OFFSET
    desired_size = None
    url = None

    while True:
        # Kullanıcı mesajlarını al
        response = requests.get(f"{telegramurl}/getUpdates?offset={OFFSET}")
        if response.status_code != 200:
            print("Mesajlar alınamadı:", response.text)
            continue
        
        updates = response.json()["result"]
        if not updates:
            time.sleep(2)
            continue
        
        for update in updates:
            OFFSET = update["update_id"] + 1
            message = update.get("message")
            if not message:
                continue
            
            # Assuming message contains a "date" field with the timestamp
            timestamp = message["date"]

            # Convert Unix timestamp to datetime object
            message_date = datetime.fromtimestamp(timestamp)

            # Skip the message if it's older than the bot's start date
            if message_date < bot_start_date:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text")

            if not text:
                continue
            
            # Kullanıcıdan URL alma
            if text.lower().startswith("url:"):
                url = text.split(":", 1)[1].strip()
                send_telegram_message(f"Ürün URL'si alındı: {url}")
            
            # Kullanıcıdan beden bilgisi alma ve eşleme

            elif text.lower() == "iptal":
                send_telegram_message("İşlem iptal edildi.")
                url, desired_size = None, None
                send_inits()
                continue

            elif text.lower().startswith("beden:"):
                size_input = text.split(":", 1)[1].strip().lower()  # Küçük harfe dönüştür
                desired_size = size_mapping.get(size_input)  # Eşleme tablosundan al
                
                if desired_size:
                    send_telegram_message(f"Beden bilgisi alındı: {desired_size}")
                else:
                    send_telegram_message(f"Geçersiz beden girdiniz: {size_input}. Geçerli bedenler: S, M, L, XL.")
                    continue
            
        # URL ve beden alındıysa stok kontrolüne başla
        if url and desired_size:
            send_telegram_message(f"Stok kontrolü başlıyor: {url} - {desired_size}")
            if ZaraChecker.check_product_availability(url, desired_size):
                send_telegram_message(f"🚨 {desired_size} bedeni stokta! Link: {url}")
                url, desired_size = None, None
                break
            #else:
            #    send_telegram_message(f"{desired_size} bedeni stokta değil, tekrar kontrol ediliyor...")
            time.sleep(60)  # 60 saniyede bir kontrol

        time.sleep(1)