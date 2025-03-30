import requests
import time

TOKEN = "7252944407:AAGOWJeR_eWFQfY2hRrgDhJJ-POOZsqA6Go"
URL = f"https://api.telegram.org/bot{TOKEN}/getMe"

while True:
    requests.get(URL)  # API को बार-बार Call करना
    time.sleep(0.1)  # 100ms का छोटा Delay ताकि जल्दी Rate Limit Cross हो जाए
