# 'pip install -r requirements.txt'     -komutunu yazınız
# chromedriver yüklemek gerekli: https://googlechromelabs.github.io/chrome-for-testing/#stable
# sonrasında indirilen doysa zipten çıkarılıp çevre değişkenlerine path olarak eklenmeli
# IP çekmek için

import requests
from bs4 import BeautifulSoup  # Kurulması gerek. Komut: pip install beautifulsoup4
import time
import subprocess
from selenium import webdriver  # Kurulması gerek. Komut: pip install selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

print("WiFi ağına bağlanılıyor...")

# Değişkenleri ayarla (SSID ve şifre)
SSID = "wifi name"
Sifre = "wifi password"
USERNAME = "web login username"
PASSWORD_WEB = "web login password"
ip = ""
driver = None


def wifi_connect_func():
    global ip, driver
    # WiFi ağına bağlan
    baglanma_komutu = f'netsh wlan connect name="{SSID}" ssid="{SSID}" interface="Wi-Fi"'
    baglanma_sonucu = subprocess.run(baglanma_komutu, shell=True)

    # Eğer ağa bağlanma başarısız olursa, hata mesajı göster
    if baglanma_sonucu.returncode != 0:
        print("WiFi ağına bağlanma başarısız oldu.")
        input("Devam etmek için bir tuşa basın...")
        exit()
    time.sleep(5)
    print("WiFi ağına başarıyla bağlandı.")
    time.sleep(5)
    # ---------------------------------------------------------
    # İstenilen web sitesinden veri çekme

    url = "https://internet.konya.bel.tr/"
    response = requests.get(url)

    # HTML içeriğini parse etme
    parsed_html = BeautifulSoup(response.text, 'html.parser')

    # "inner cover" sınıfındaki <h3> etiketini bulma
    h3_etiketi = parsed_html.find(class_="inner cover").find('h3')

    # <h3> etiketinin içindeki <b> etiketinin metin içeriğine erişme
    ip = h3_etiketi.find('b')
    print(ip.text)
    # time.sleep(10)

    web_url = "http://10.254.0.254:1000/login?" + ip.text
    print(web_url)
    time.sleep(5)
    # ---------------------------------------------------------
    try:
        # Selenium kullanarak web sayfasına giriş yapma
        driver = webdriver.Chrome()  # Webdriver'ı çalıştır
        driver.get(web_url)  # Web sayfasını aç
        username_field = driver.find_element(By.NAME, "username")  # Kullanıcı adı alanını bul
        username_field.send_keys(USERNAME)  # Kullanıcı adını gir
        password_field = driver.find_element(By.NAME, "password")  # Şifre alanını bul
        password_field.send_keys(PASSWORD_WEB)  # Şifreyi gir
        password_field.send_keys(Keys.RETURN)  # Enter tuşuna bas
        print("Web sayfasına giriş yapıldı.")

    except Exception as e:
        print("Web sayfasına giriş yapılırken hata oluştu:", e)
    finally:
        # Tarayıcıyı kapat
        driver.quit()


#   -------------------------ALTTAKİ İKİ SATIR GEREKİ OLMAYABİLİR WHILE İÇERİSİNE EKLEMEYE ÇALIŞ

# Bağlantıyı 30 saniyede bir kontrol et
while True:
    wifi_connect_func()
    time.sleep(50)
    print("kontrol edildi")



