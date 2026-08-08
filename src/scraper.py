from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import csv
import re

URLS = [
    "https://divar.ir/s/tehran/buy-apartment",
    "https://divar.ir/s/tehran/buy-apartment/abshar",
    "https://divar.ir/s/tehran/buy-apartment/ajudaniye",
    "https://divar.ir/s/tehran/buy-apartment/ararat",
]

def extract_meterage(title):
    match = re.search(r'(\d+)\s*/?\s*متر', title)
    if match:
        return match.group(1)
    match = re.search(r'(\d{2,3})\s*م(?:تر)?[^ی]', title)
    if match:
        return match.group(1)
    return None

def extract_district(bottom_text):
    match = re.search(r'در\s+(.+)$', bottom_text)
    if match:
        return match.group(1).strip()
    return None

service = Service(r"msedgedriver.exe")
driver = webdriver.Edge(service=service)

listings = []
seen_links = set()

def collect_current_cards():
    cards = driver.find_elements(By.CLASS_NAME, "kt-post-card")
    new_count = 0
    for card in cards:
        try:
            title = card.find_element(By.CLASS_NAME, "kt-post-card__title").text
            price = card.find_element(By.CLASS_NAME, "kt-post-card__description").text
            link = card.find_element(By.CLASS_NAME, "kt-post-card__action").get_attribute("href")

            if link in seen_links:
                continue
            seen_links.add(link)

            try:
                bottom_text = card.find_element(By.CLASS_NAME, "kt-post-card__bottom-description").text
            except:
                bottom_text = ""

            meterage = extract_meterage(title)
            district = extract_district(bottom_text)

            listings.append({
                "title": title,
                "price": price,
                "meterage": meterage,
                "district": district,
                "link": link
            })
            new_count += 1
        except Exception:
            pass
    return new_count

for url in URLS:
    print(f"\n=== شروع اسکرپینگ: {url} ===")
    driver.get(url)
    time.sleep(5)

    scroll_container = driver.execute_script("""
        let all = document.querySelectorAll('*');
        let best = null;
        let maxDiff = 0;
        for (let el of all) {
            let diff = el.scrollHeight - el.clientHeight;
            if (diff > maxDiff && el.clientHeight > 200 && el.clientHeight < 800) {
                maxDiff = diff;
                best = el;
            }
        }
        return best;
    """)

    collect_current_cards()

    for i in range(15):
        if scroll_container:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_container)
        else:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_items = collect_current_cards()
        print(f"اسکرول {i+1}/15 - آگهی جدید: {new_items} - مجموع کل: {len(listings)}")
        if new_items == 0 and i > 3:
            break  # اگه چند بار پشت‌سرهم آگهی جدید نیومد، برو سراغ منطقه بعدی

driver.quit()

with open("data/listings.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "meterage", "district", "link"])
    writer.writeheader()
    writer.writerows(listings)

print(f"\n✅ مجموع نهایی: {len(listings)} آگهی منحصربه‌فرد ذخیره شد در data/listings.csv")