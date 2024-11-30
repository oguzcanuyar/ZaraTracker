import requests
from bs4 import BeautifulSoup
import time
import telegramManager

def check_product_availability(url, desired_size):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Sayfa alınamadı, HTTP Kodu:", response.status_code)
            return False
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Tüm bedenleri bul
        size_elements = soup.find_all("li", class_="size-selector-sizes__size")
        
        if not size_elements:
            print("Beden bilgisi bulunamadı.")
            return False
        
        for size_element in size_elements:
            size_label = size_element.find("div", class_="size-selector-sizes-size__label")
            if size_label and desired_size in size_label.text:
                data_qa_action = size_element.find("button").get("data-qa-action", "")
                if data_qa_action == "size-in-stock":
                    print(f"{desired_size} bedeni stokta!")
                    return True
                elif data_qa_action == "size-out-of-stock":
                    print(f"{desired_size} bedeni stokta değil.")
                    return False

        print(f"{desired_size} bedeni bulunamadı.")
        return False
    
    except Exception as e:
        print("Hata:", e)
        return False

# Botu çalıştır
url = "https://www.zara.com/tr/tr/jakar-crop-kesim-ceket-p04575303.html?v1=404683843&v2=2467336"
desired_size = "XL (US XL)"

# Belirli aralıklarla kontrol

initial=True
while True:
    if initial:
        initial = False
        message = f"Bot başlatılıyor... Beden : {desired_size} Link : {url}"
        telegramManager.send_telegram_message(message)

    if check_product_availability(url, desired_size):
        print(f"{desired_size} bedeni stokta!")
        message = f"🚨 {desired_size} bedeni stokta! Link: {url}"
        telegramManager.send_telegram_message(message)
        break
    else:
        print(f"{desired_size} bedeni stokta değil, tekrar kontrol ediliyor...")
    time.sleep(60)  # 60 saniyede bir kontrol et
