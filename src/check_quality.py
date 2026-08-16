import pandas as pd

df = pd.read_csv("data/listings_detailed.csv")

print("تعداد کل ردیف‌ها:", len(df))
print("\n--- درصد پر بودن هر ستون ---")
for col in df.columns:
    filled_percent = (df[col].notnull().sum() / len(df)) * 100
    print(f"{col}: {filled_percent:.1f}% پر شده")

print("\n--- نمونه‌ای از ۵ ردیف اول ---")
print(df[['title', 'floor', 'build_year', 'rooms']].head(10))