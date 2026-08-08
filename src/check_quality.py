import pandas as pd

df = pd.read_csv("data/listings.csv")

print("تعداد کل ردیف‌ها:", len(df))
print("\n--- تعداد مقادیر خالی (None) در هر ستون ---")
print(df.isnull().sum())

print("\n--- درصد پر بودن هر ستون ---")
for col in df.columns:
    filled_percent = (df[col].notnull().sum() / len(df)) * 100
    print(f"{col}: {filled_percent:.1f}% پر شده")

print("\n--- نمونه‌ای از ۵ ردیف اول ---")
print(df.head())

print("\n--- تعداد لینک‌های تکراری (باید صفر باشه) ---")
print(df['link'].duplicated().sum())
print("\n--- عنوان‌هایی که متراژ ازشون استخراج نشده ---")
missing_meterage = df[df['meterage'].isnull()]
for title in missing_meterage['title']:
    print("-", title)