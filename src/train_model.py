import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_csv("data/listings_clean.csv")

# گروه‌بندی مناطق کم‌تکرار به دسته‌ی "سایر"
district_counts = df['district'].value_counts()
frequent_districts = district_counts[district_counts >= 5].index
df['district_grouped'] = df['district'].apply(lambda x: x if x in frequent_districts else 'سایر')

print("تعداد مناطق بعد از گروه‌بندی:", df['district_grouped'].nunique())

# --- مدل اول: فقط متراژ ---
X1 = df[['meterage']]
y = df['price']

X1_train, X1_test, y_train, y_test = train_test_split(X1, y, test_size=0.2, random_state=42)

model1 = LinearRegression()
model1.fit(X1_train, y_train)
pred1 = model1.predict(X1_test)

mae1 = mean_absolute_error(y_test, pred1)
r2_1 = r2_score(y_test, pred1)
mean_price = y_test.mean()

print("=== مدل اول: فقط با متراژ ===")
print(f"MAE: {mae1:,.0f} تومان ({(mae1/mean_price)*100:.1f}% از میانگین)")
print(f"R²: {r2_1:.3f}")

# --- مدل دوم: متراژ + منطقه ---
df_encoded = pd.get_dummies(df, columns=['district_grouped'], drop_first=True)
feature_cols = ['meterage'] + [col for col in df_encoded.columns if col.startswith('district_grouped_')]

feature_cols = ['meterage'] + [col for col in df_encoded.columns if col.startswith('district_')]
X2 = df_encoded[feature_cols]

X2_train, X2_test, y_train2, y_test2 = train_test_split(X2, y, test_size=0.2, random_state=42)

model2 = LinearRegression()
model2.fit(X2_train, y_train2)
pred2 = model2.predict(X2_test)

mae2 = mean_absolute_error(y_test2, pred2)
r2_2 = r2_score(y_test2, pred2)

print("\n=== مدل دوم: متراژ + منطقه ===")
print(f"MAE: {mae2:,.0f} تومان ({(mae2/mean_price)*100:.1f}% از میانگین)")
print(f"R²: {r2_2:.3f}")

print("\n=== مقایسه‌ی بهبود ===")
print(f"بهبود R²: {r2_1:.3f} → {r2_2:.3f}")
print(f"بهبود خطا: {(mae1/mean_price)*100:.1f}% → {(mae2/mean_price)*100:.1f}%")

print("\n=== بررسی توزیع مناطق ===")
print("تعداد مناطق منحصربه‌فرد:", df['district'].nunique())
print("\nتوزیع تعداد آگهی در هر منطقه:")
print(df['district'].value_counts().describe())