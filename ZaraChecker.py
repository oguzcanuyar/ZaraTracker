import requests
from bs4 import BeautifulSoup
import time

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