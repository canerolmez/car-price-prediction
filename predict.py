import joblib
import pandas as pd


model = joblib.load("car_price_model.pkl")

print("Araç bilgilerini giriniz:")

konum = input("Konum: ")
marka = input("Marka: ")
seri = input("Seri: ")
model_adi = input("Model: ")

yil = int(input("Yıl: "))
kilometre = float(input("Kilometre: "))

vites_tipi = input("Vites tipi: ")
yakit_tipi = input("Yakıt tipi: ")
kasa_tipi = input("Kasa tipi: ")

motor_hacmi = float(input("Motor hacmi: "))
motor_gucu = float(input("Motor gücü: "))

cekis = input("Çekiş tipi: ")

ortalama_yakit_tuketimi = float(
    input("Ortalama yakıt tüketimi: ")
)

yakit_deposu = float(
    input("Yakıt deposu (litre): ")
)

tramer = float(input("Tramer tutarı: "))
degisen = int(input("Değişen parça sayısı: "))
boyali = int(input("Boyalı parça sayısı: "))


# Yeni özellikleri hesapla
arac_yasi = 2026 - yil
arac_yasi = max(arac_yasi, 1)

yillik_km = kilometre / arac_yasi


# Modelin beklediği araç verisini oluştur
arac = pd.DataFrame([
    {
        "konum": konum,
        "marka": marka,
        "seri": seri,
        "model": model_adi,
        "yil": yil,
        "kilometre": kilometre,
        "vites_tipi": vites_tipi,
        "yakit_tipi": yakit_tipi,
        "kasa_tipi": kasa_tipi,
        "motor_hacmi": motor_hacmi,
        "motor_gucu": motor_gucu,
        "cekis": cekis,
        "ortalama_yakit_tuketimi": ortalama_yakit_tuketimi,
        "yakit_deposu": yakit_deposu,
        "tramer": tramer,
        "degisen": degisen,
        "boyali": boyali,
        "arac_yasi": arac_yasi,
        "yillik_km": yillik_km
    }
])


# Fiyat tahmini yap
tahmin = model.predict(arac)

print()
print("------------------------------")
print("Tahmini araç fiyatı:", round(tahmin[0], 2), "TL")
print("------------------------------")