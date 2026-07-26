from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import csv

service = Service(r"msedgedriver.exe")
driver = webdriver.Edge(service=service)

url = "https://divar.ir/s/tehran/buy-apartment"
driver.get(url)
time.sleep(5)

cards = driver.find_elements(By.CLASS_NAME, "kt-post-card")
print("تعداد کارت‌های پیدا شده:", len(cards))

listings = []

for i, card in enumerate(cards, start=1):
    try:
        title = card.find_element(By.CLASS_NAME, "kt-post-card__title").text
        price = card.find_element(By.CLASS_NAME, "kt-post-card__description").text
        link = card.find_element(By.CLASS_NAME, "kt-post-card__action").get_attribute("href")

        print(f"\n--- آگهی {i} ---")
        print("عنوان:", title)
        print("قیمت:", price)
        print("لینک:", link)

        listings.append({
            "title": title,
            "price": price,
            "link": link
        })

    except Exception as e:
        print(f"آگهی {i}: خطا در استخراج -", e)

driver.quit()

# ذخیره در فایل CSV
with open("data/listings.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "link"])
    writer.writeheader()
    writer.writerows(listings)

print(f"\n✅ {len(listings)} آگهی ذخیره شد در data/listings.csv")