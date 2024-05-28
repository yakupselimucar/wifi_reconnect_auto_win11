# 'pip install -r requirements.txt'     -write in the terminal
# chromedriver must be installed: https://googlechromelabs.github.io/chrome-for-testing/#stable
# after downloading the chromedriver, you need to add the path to the chromedriver.exe file to the system environment variables.

# to pull the ip address 
import requests
from bs4 import BeautifulSoup  # it must be installed. Command: pip install beautifulsoup4
import time
import subprocess
from selenium import webdriver  # it must be installed. Command: pip install selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

print("connecting to the WiFi network...")

# adjust the following variables according to your own information
SSID = "wifi name"
Sifre = "wifi password"
USERNAME = "web login username"
PASSWORD_WEB = "web login password"
ip = ""  # it should be empty at the beginning
driver = None


def wifi_connect_func():
    global ip, driver
    # connect to the WiFi network
    baglanma_komutu = f'netsh wlan connect name="{SSID}" ssid="{SSID}" interface="Wi-Fi"'
    baglanma_sonucu = subprocess.run(baglanma_komutu, shell=True)

    # if the connection is not successful, print an error message and exit the program
    if baglanma_sonucu.returncode != 0:
        print("Error: Could not connect to the WiFi network. Please check the SSID and password.")
        input("to continue press enter...")
        exit()
    time.sleep(5)
    print("Successfully connected to the WiFi network...")
    time.sleep(5)
    # ---------------------------------------------------------
    
    # pull data from the desired web page
    url = "Paste here the URL of the website from which the ip will be retrieved" # I wrote this to pull the ip directly from the site because the ip address at the end of the url I use for web logging is constantly changing. 
    response = requests.get(url)

    # Parse HTML content
    parsed_html = BeautifulSoup(response.text, 'html.parser')

    # Find the <h3> tag in the “inner cover” class
    h3_etiketi = parsed_html.find(class_="inner cover").find('h3')

    # Access the text content of the <b> tag inside the <h3> tag
    ip = h3_etiketi.find('b')
    print(ip.text)
    # time.sleep(10)

    web_url = "The url of the page to be logged in" + ip.text # We create the url of the page to be web logged by adding the ip address received with ip.text to the url of the page to be web logged.
    print(web_url)
    time.sleep(5)
    # ---------------------------------------------------------
    try:
        # Use Selenium to log into the web page
        driver = webdriver.Chrome()                                # Run the Webdriver
        driver.get(web_url)                                        # Open the web page
        username_field = driver.find_element(By.NAME, "username")  # Find the username field
        username_field.send_keys(USERNAME)                         # Enter the username
        password_field = driver.find_element(By.NAME, "password")  # Find the password field
        password_field.send_keys(PASSWORD_WEB)                     # Enter the password
        password_field.send_keys(Keys.RETURN)                      # Click "Enter"
        print("Entered the web page...")

    except Exception as e:
        print("An error occurred while logging into the web page:", e)
    finally:
        # exit browser
        driver.quit()


# Check the connection every 100 seconds
while True:
    wifi_connect_func()
    time.sleep(100)
    print("connection checked...")



