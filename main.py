import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score



cars = pd.read_csv("data/cars1.csv")

cars = cars.rename(columns={"ls datakonum": "konum"})


# Yeni özellikler
cars["arac_yasi"] = 2026 - cars["yil"]
cars["arac_yasi"] = cars["arac_yasi"].clip(lower=1)

cars["yillik_km"] = cars["kilometre"] / cars["arac_yasi"]


# Aşırı kilometre değerlerini temizle
cars = cars[cars["yillik_km"] <= 200000]


# Eksik motor bilgilerini temizle
cars = cars.dropna(subset=["motor_hacmi", "motor_gucu"])


# X = modelin kullanacağı özellikler
# y = modelin tahmin edeceği fiyat
X = cars.drop(columns=["fiyat"])
y = cars["fiyat"]


# Veriyi eğitim ve test olarak ayır
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Kategorik ve sayısal sütunları ayır
categorical_columns = X.select_dtypes(
    include=["object", "str"]
).columns

numeric_columns = X.select_dtypes(
    exclude=["object", "str"]
).columns


# Metin sütunlarını modele uygun sayısal hale getir
preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        ),
        (
            "num",
            "passthrough",
            numeric_columns
        )
    ]
)


# Modeli oluştur
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "regressor",
            RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)


print("Model eğitiliyor...")

model.fit(X_train, y_train)

print("Model eğitildi.")
# Test verisi üzerinde tahmin yap
y_pred = model.predict(X_test)

# Model başarısını ölç
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("RMSE:", rmse)
print("R2:", r2)
sonuclar = X_test[["marka", "seri", "model", "yil", "kilometre"]].copy()

sonuclar["gercek_fiyat"] = y_test
sonuclar["tahmin_fiyat"] = y_pred

print(
    sonuclar[
        ["marka", "seri", "model", "yil",
         "kilometre", "gercek_fiyat", "tahmin_fiyat"]
    ].head(10)
)
joblib.dump(model, "car_price_model.pkl")

print("Model kaydedildi.")