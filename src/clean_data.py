import pandas as pd

df = pd.read_csv("data/listings.csv")

print("تعداد ردیف‌ها و ستون‌ها:", df.shape)
print("\n--- نوع داده هر ستون ---")
print(df.dtypes)

print("\n--- نمونه‌ای از ستون price (خام) ---")
print(df['price'].head(10))

print("\n--- نمونه‌ای از ستون meterage (خام) ---")
print(df['meterage'].head(10))

import re

def normalize_digits(text):
    """تبدیل ارقام فارسی/عربی به انگلیسی"""
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"
    
    text = str(text)
    for p, e in zip(persian_digits, english_digits):
        text = text.replace(p, e)
    for a, e in zip(arabic_digits, english_digits):
        text = text.replace(a, e)
    return text

def clean_price(price_text):
    """تبدیل قیمت متنی به عدد (تومان)"""
    if pd.isna(price_text):
        return None
    text = normalize_digits(price_text)
    # فقط ارقام رو نگه دار (کاما، فاصله، "تومان" رو حذف کن)
    digits_only = re.sub(r'[^\d]', '', text)
    if digits_only == '':
        return None
    return int(digits_only)

def clean_meterage(meterage_text):
    """تبدیل متراژ متنی به عدد"""
    if pd.isna(meterage_text):
        return None
    text = normalize_digits(meterage_text)
    digits_only = re.sub(r'[^\d]', '', text)
    if digits_only == '':
        return None
    return int(digits_only)

# اعمال این توابع روی کل دیتافریم
df['price_clean'] = df['price'].apply(clean_price)
df['meterage_clean'] = df['meterage'].apply(clean_meterage)

print("\n--- بعد از تمیزکاری ---")
print(df[['price', 'price_clean', 'meterage', 'meterage_clean']].head(10))

print("\n--- نوع داده جدید ---")
print(df[['price_clean', 'meterage_clean']].dtypes)

print("\n--- آمار کلی price_clean ---")
print(df['price_clean'].describe())

print("\n--- آمار کلی meterage_clean ---")
print(df['meterage_clean'].describe())

print("\n--- ۵ آگهی با کمترین قیمت ---")
print(df.nsmallest(5, 'price_clean')[['title', 'price_clean', 'meterage_clean']])

print("\n--- ۵ آگهی با بیشترین قیمت ---")
print(df.nlargest(5, 'price_clean')[['title', 'price_clean', 'meterage_clean']])

df_final = df[['title', 'price_clean', 'meterage_clean', 'district', 'link']].copy()
df_final = df_final.rename(columns={'price_clean': 'price', 'meterage_clean': 'meterage'})

# حذف ردیف‌هایی که قیمت یا متراژ ندارن (چون برای مدل ضروری هستن)
df_final_no_na = df_final.dropna(subset=['price', 'meterage'])

print(f"\nتعداد ردیف‌ها قبل از حذف NaN: {len(df_final)}")
print(f"تعداد ردیف‌ها بعد از حذف NaN: {len(df_final_no_na)}")

df_final_no_na.to_csv("data/listings_clean.csv", index=False, encoding="utf-8-sig")
print("\n✅ فایل تمیز ذخیره شد در data/listings_clean.csv")