import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_csv("data/listings_model_ready.csv")

# گروه‌بندی مناطق کم‌تکرار
district_counts = df['district'].value_counts()
frequent_districts = district_counts[district_counts >= 5].index
df['district_grouped'] = df['district'].apply(lambda x: x if x in frequent_districts else 'سایر')

y = df['price']
mean_price = y.mean()

def run_model(feature_cols, df_encoded, label):
    X = df_encoded[feature_cols]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"=== {label} ===")
    print(f"MAE: {mae:,.0f} تومان ({(mae/mean_price)*100:.1f}% از میانگین)")
    print(f"R²: {r2:.3f}\n")
    return r2, mae

# --- مدل ۱: فقط متراژ ---
r2_1, mae_1 = run_model(['meterage'], df, "مدل ۱: فقط متراژ")

# --- مدل ۲: متراژ + منطقه ---
df_enc2 = pd.get_dummies(df, columns=['district_grouped'], drop_first=True)
cols2 = ['meterage'] + [c for c in df_enc2.columns if c.startswith('district_grouped_')]
r2_2, mae_2 = run_model(cols2, df_enc2, "مدل ۲: متراژ + منطقه")

# --- مدل ۳: متراژ + منطقه + طبقه + سال ساخت + اتاق ---
df_enc3 = pd.get_dummies(df, columns=['district_grouped'], drop_first=True)
cols3 = ['meterage', 'floor', 'build_year', 'rooms'] + [c for c in df_enc3.columns if c.startswith('district_grouped_')]
r2_3, mae_3 = run_model(cols3, df_enc3, "مدل ۳: همه‌ی فیچرها")

print("=== مقایسه‌ی نهایی ===")
print(f"مدل ۱ (فقط متراژ):        R²={r2_1:.3f}  |  خطا={mae_1/mean_price*100:.1f}%")
print(f"مدل ۲ (+ منطقه):          R²={r2_2:.3f}  |  خطا={mae_2/mean_price*100:.1f}%")
print(f"مدل ۳ (+ طبقه/سال/اتاق):  R²={r2_3:.3f}  |  خطا={mae_3/mean_price*100:.1f}%")