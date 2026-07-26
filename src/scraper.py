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

# پیدا کردن container قابل‌اسکرول به‌صورت خودکار (با جاوااسکریپت)
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

SCROLL_COUNT = 20
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
            listings.append({"title": title, "price": price, "link": link})
            new_count += 1
        except Exception:
            pass
    return new_count

collect_current_cards()

for i in range(SCROLL_COUNT):
    if scroll_container:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_container)
    else:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_items = collect_current_cards()
    print(f"اسکرول {i+1}/{SCROLL_COUNT} - آگهی جدید: {new_items} - مجموع: {len(listings)}")

driver.quit()

with open("data/listings.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "link"])
    writer.writeheader()
    writer.writerows(listings)

print(f"\n✅ {len(listings)} آگهی منحصربه‌فرد ذخیره شد در data/listings.csv")