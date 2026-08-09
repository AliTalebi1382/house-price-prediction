import pandas as pd
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display

def fa(text):
    """آماده‌سازی متن فارسی برای نمایش درست در نمودار"""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

df = pd.read_csv("data/listings_clean.csv")

# تنظیم فونت برای پشتیبانی از فارسی
plt.rcParams['font.family'] = 'Tahoma'

# نمودار ۱: رابطه‌ی متراژ و قیمت
plt.figure(figsize=(10, 6))
plt.scatter(df['meterage'], df['price'] / 1_000_000_000, alpha=0.5, color='#1a3a5c')
plt.xlabel(fa('متراژ (متر مربع)'))
plt.ylabel(fa('قیمت (میلیارد تومان)'))
plt.title(fa('رابطه‌ی متراژ و قیمت آپارتمان‌های تهران'))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('results/price_vs_meterage.png', dpi=150)
print("✅ نمودار اول ذخیره شد: results/price_vs_meterage.png")
plt.show()

# نمودار ۲: میانگین قیمت ۱۵ منطقه‌ی گرون‌ترین
avg_price_by_district = df.groupby('district')['price'].mean().sort_values(ascending=False) / 1_000_000_000
top_15 = avg_price_by_district.head(15)

plt.figure(figsize=(10, 6))
top_15.plot(kind='bar', color='#1a3a5c')
plt.xlabel(fa('منطقه'))
plt.ylabel(fa('میانگین قیمت (میلیارد تومان)'))
plt.title(fa('۱۵ منطقه‌ی گرون‌ترین (بر اساس داده‌های جمع‌آوری‌شده)'))
plt.xticks(ticks=range(len(top_15)), 
           labels=[fa(d) for d in top_15.index], 
           rotation=45, ha='right')
plt.tight_layout()
plt.savefig('results/price_by_district.png', dpi=150)
print("✅ نمودار دوم ذخیره شد: results/price_by_district.png")
# plt.show()  # غیرفعال کردیم تا cmd قفل نشه