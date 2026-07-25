from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time

service = Service(r"msedgedriver.exe")
driver = webdriver.Edge(service=service)

url = "https://divar.ir/s/tehran/buy-apartment"
driver.get(url)
time.sleep(5)

cards = driver.find_elements(By.CLASS_NAME, "kt-post-card")
print("تعداد کارت‌های پیدا شده:", len(cards))

for i, card in enumerate(cards, start=1):
    try:
        title = card.find_element(By.CLASS_NAME, "kt-post-card__title").text
        price = card.find_element(By.CLASS_NAME, "kt-post-card__description").text
        print(f"\n--- آگهی {i} ---")
        print("عنوان:", title)
        print("قیمت:", price)
    except Exception as e:
        print(f"آگهی {i}: خطا در استخراج -", e)

driver.quit()