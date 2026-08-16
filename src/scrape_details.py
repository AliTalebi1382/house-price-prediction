from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
import csv

df = pd.read_csv("data/listings_clean.csv")
print(f"تعداد آگهی برای پردازش: {len(df)}")

service = Service(r"msedgedriver.exe")
driver = webdriver.Edge(service=service)

detailed_listings = []

for idx, row in df.iterrows():
    link = row['link']
    print(f"\n[{idx+1}/{len(df)}] در حال پردازش: {link[:60]}...")

    detail = {
        "title": row['title'],
        "price": row['price'],
        "meterage": row['meterage'],
        "district": row['district'],
        "link": link,
        "floor": None,
        "build_year": None,
        "rooms": None,
    }

    try:
        driver.get(link)
        time.sleep(3)

        # بخش اول: قیمت، قیمت هر متر، طبقه
        try:
            rows_info = driver.find_elements(By.CLASS_NAME, "kt-unexpandable-row")
            for r in rows_info:
                try:
                    title_text = r.find_element(By.CLASS_NAME, "kt-unexpandable-row__title").text
                    value_text = r.find_element(By.CLASS_NAME, "kt-unexpandable-row__value").text
                    if "طبقه" in title_text:
                        detail["floor"] = value_text
                except:
                    pass
        except:
            pass

        # بخش دوم: جدول متراژ، ساخت، اتاق
        try:
            table = driver.find_element(By.CLASS_NAME, "kt-group-row")
            headers = [h.text for h in table.find_elements(By.CLASS_NAME, "kt-group-row-item__title")]
            values = [v.text for v in table.find_elements(By.CLASS_NAME, "kt-group-row-item__value")]

            for h, v in zip(headers, values):
                if "ساخت" in h:
                    detail["build_year"] = v
                elif "اتاق" in h:
                    detail["rooms"] = v
        except:
            pass

        print(f"  → طبقه: {detail['floor']}, سال ساخت: {detail['build_year']}, اتاق: {detail['rooms']}")

    except Exception as e:
        print(f"  خطا در پردازش این آگهی: {e}")

    detailed_listings.append(detail)

driver.quit()

with open("data/listings_detailed.csv", "w", newline="", encoding="utf-8-sig") as f:
    fieldnames = ["title", "price", "meterage", "district", "link", "floor", "build_year", "rooms"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(detailed_listings)

print(f"\n✅ {len(detailed_listings)} آگهی با جزئیات کامل ذخیره شد در data/listings_detailed.csv")