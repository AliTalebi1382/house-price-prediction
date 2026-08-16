from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time

service = Service(r"msedgedriver.exe")
driver = webdriver.Edge(service=service)

# یکی از لینک‌های واقعی خودت رو اینجا جایگزین کن
url = "لینک یکی از آگهی‌ها از فایل CSV"
driver.get("https://divar.ir/v/%DB%B6%DB%B5-%D9%85%D8%AA%D8%B1%DB%8C-%D8%A8%D8%A7-%D9%BE%D8%A7%D8%B1%DA%A9%DB%8C%D9%86%DA%AF-%D8%AF%D8%B1-%D9%85%D8%AD%D9%84%D9%87-%D8%A2%D8%A8%D8%B4%D8%A7%D8%B1/gac1M8N9?tracker_session_id=ea4f2a8c-10f7-46e9-888e-8887426c37dd_gac1M8N9_N")
time.sleep(4)

rows = driver.find_elements(By.CLASS_NAME, "kt-unexpandable-row")
print(f"تعداد ردیف مشخصات پیدا شده: {len(rows)}\n")

for row in rows:
    try:
        title = row.find_element(By.CLASS_NAME, "kt-unexpandable-row__title").text
        value = row.find_element(By.CLASS_NAME, "kt-unexpandable-row__value").text
        print(f"{title}: {value}")
    except Exception as e:
        print("خطا در یک ردیف:", e)
 
print("\n--- جدول مشخصات (متراژ، ساخت، اتاق) ---")
try:
    table = driver.find_element(By.CLASS_NAME, "kt-group-row")
    headers = table.find_elements(By.CLASS_NAME, "kt-group-row-item__title")
    values = table.find_elements(By.CLASS_NAME, "kt-group-row-item__value")
    
    header_texts = [h.text for h in headers]
    value_texts = [v.text for v in values]
    
    print("عنوان‌ها:", header_texts)
    print("مقادیر:", value_texts)
except Exception as e:
    print("خطا در پیدا کردن جدول:", e)
driver.quit()