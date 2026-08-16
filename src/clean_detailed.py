import pandas as pd
import re

df = pd.read_csv("data/listings_detailed.csv")

def normalize_digits(text):
    if pd.isna(text):
        return None
    persian = "۰۱۲۳۴۵۶۷۸۹"
    arabic = "٠١٢٣٤٥٦٧٨٩"
    english = "0123456789"
    text = str(text)
    for p, e in zip(persian, english):
        text = text.replace(p, e)
    for a, e in zip(arabic, english):
        text = text.replace(a, e)
    return text

def clean_floor(floor_text):
    """طبقه رو چه به‌شکل '۲' باشه چه '۳ از ۵'، فقط عدد طبقه رو برمی‌گردونه"""
    if pd.isna(floor_text):
        return None
    text = normalize_digits(floor_text)
    match = re.search(r'-?\d+', text)
    if match:
        return int(match.group())
    return None

def clean_number(text):
    """برای build_year و rooms - فقط عدد خالص"""
    if pd.isna(text):
        return None
    text = normalize_digits(text)
    digits_only = re.sub(r'[^\d]', '', text)
    if digits_only == '':
        return None
    return int(digits_only)

df['floor_clean'] = df['floor'].apply(clean_floor)
df['build_year_clean'] = df['build_year'].apply(clean_number)
df['rooms_clean'] = df['rooms'].apply(clean_number)

print("--- نمونه‌ای بعد از تمیزکاری ---")
print(df[['floor', 'floor_clean', 'build_year', 'build_year_clean', 'rooms', 'rooms_clean']].head(10))

print("\n--- بررسی مقادیر غیرمنطقی ---")
print("سال ساخت خارج از بازه‌ی منطقی (1300-1405):")
print(df[(df['build_year_clean'] < 1300) | (df['build_year_clean'] > 1405)][['title', 'build_year_clean']])

# ساخت فایل نهایی برای مدل
df_final = df[['title', 'price', 'meterage', 'district', 'floor_clean', 'build_year_clean', 'rooms_clean', 'link']].copy()
df_final = df_final.rename(columns={
    'floor_clean': 'floor',
    'build_year_clean': 'build_year',
    'rooms_clean': 'rooms'
})

# فقط ردیف‌هایی که همه‌ی فیچرهای اصلی رو دارن نگه می‌داریم
df_model_ready = df_final.dropna(subset=['price', 'meterage', 'floor', 'build_year', 'rooms'])

print(f"\nتعداد ردیف قبل از حذف خالی‌ها: {len(df_final)}")
print(f"تعداد ردیف آماده برای مدل: {len(df_model_ready)}")

df_model_ready.to_csv("data/listings_model_ready.csv", index=False, encoding="utf-8-sig")
print("\n✅ فایل نهایی ذخیره شد در data/listings_model_ready.csv")