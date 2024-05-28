# 'pip install -r requirements.txt'     -komutunu yazınız
# chromedriver yüklemek gerekli: https://googlechromelabs.github.io/chrome-for-testing/#stable
# sonrasında indirilen doysa zipten çıkarılıp çevre değişkenlerine path olarak eklenmeli
# IP çekmek için


import requests
from bs4 import BeautifulSoup
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

SSID = "Kbb-WiLokal"
Sifre = "KbbW1Lokal"
USERNAME = "yari.zamanli"
PASSWORD_WEB = "Bm12345."
driver = None


def connect_to_wifi():
    baglanma_komutu = f'netsh wlan connect name="{SSID}" ssid="{SSID}" interface="Wi-Fi"'
    baglanma_sonucu = subprocess.run(baglanma_komutu, shell=True)
    if baglanma_sonucu.returncode != 0:
        print("WiFi ağına bağlanma başarısız oldu.")
        return False
    print("WiFi ağına başarıyla bağlandı.")
    time.sleep(5)
    return True


# İstenilen web sitesinden veri çekme
def get_ip():
    url = "https://internet.konya.bel.tr/"
    response = requests.get(url)
    parsed_html = BeautifulSoup(response.text, 'html.parser')
    h3_etiketi = parsed_html.find(class_="inner cover").find('h3')
    ip = h3_etiketi.find('b').text
    return ip


def login_to_webpage(ip):
    global driver
    web_url = f"http://10.254.0.254:1000/login?{ip}"
    print(web_url)
    try:
        # Selenium kullanarak web sayfasına giriş yapma
        driver = webdriver.Chrome()
        driver.get(web_url)
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys(USERNAME)
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(PASSWORD_WEB)
        password_field.send_keys(Keys.RETURN)
        print("Web sayfasına giriş yapıldı.")
    except Exception as e:
        print("Web sayfasına giriş yapılırken hata oluştu:", e)
    finally:
        if driver:
            driver.quit()


def main():
    while True:
        if connect_to_wifi():
            ip = get_ip()
            if ip:
                login_to_webpage(ip)
        time.sleep(12001)
        print("Tekrar Bağlanıyor!")


if __name__ == "__main__":
    main()
