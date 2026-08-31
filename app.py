import streamlit as st
import pandas as pd
import joblib


st.set_page_config(
    page_title="Araç Fiyat Tahmini",
    page_icon="🚗",
    layout="wide"
)


# -----------------------------
# MODEL VE VERİYİ YÜKLE
# -----------------------------

@st.cache_resource
def load_model():
    return joblib.load("car_price_model.pkl")


@st.cache_data
def load_data():
    df = pd.read_csv("data/cars1.csv")
    df = df.rename(columns={"ls datakonum": "konum"})
    return df


model = load_model()
cars = load_data()


# -----------------------------
# BAŞLIK
# -----------------------------

st.title("🚗 Araç Fiyat Tahmini")
st.write(
    "Araç bilgilerini girerek makine öğrenmesi modeliyle "
    "tahmini araç fiyatını öğrenebilirsiniz."
)


# -----------------------------
# MARKA
# -----------------------------

markalar = sorted(
    cars["marka"]
    .dropna()
    .unique()
)

marka = st.selectbox(
    "Marka",
    markalar
)


# -----------------------------
# SERİ
# -----------------------------

seriler = sorted(
    cars[cars["marka"] == marka]["seri"]
    .dropna()
    .unique()
)

seri = st.selectbox(
    "Seri",
    seriler
)


# -----------------------------
# MODEL
# -----------------------------

modeller = sorted(
    cars[
        (cars["marka"] == marka) &
        (cars["seri"] == seri)
    ]["model"]
    .dropna()
    .unique()
)

model_adi = st.selectbox(
    "Model",
    modeller
)


# -----------------------------
# SEÇİLEN ARACA UYGUN KAYITLAR
# -----------------------------

uygun_araclar = cars[
    (cars["marka"] == marka) &
    (cars["seri"] == seri) &
    (cars["model"] == model_adi)
]


# -----------------------------
# YIL
# -----------------------------

yillar = sorted(
    uygun_araclar["yil"]
    .dropna()
    .astype(int)
    .unique(),
    reverse=True
)

yil = st.selectbox(
    "Yıl",
    yillar
)


# Seçilen yıl dahil filtrele
yila_uygun_araclar = uygun_araclar[
    uygun_araclar["yil"] == yil
]


# -----------------------------
# OTOMATİK VARSAYILAN DEĞERLER
# -----------------------------

varsayilan_motor_hacmi = int(
    yila_uygun_araclar["motor_hacmi"]
    .dropna()
    .median()
)

varsayilan_motor_gucu = int(
    yila_uygun_araclar["motor_gucu"]
    .dropna()
    .median()
)

varsayilan_yakit_tuketimi = float(
    yila_uygun_araclar["ortalama_yakit_tuketimi"]
    .dropna()
    .median()
)

varsayilan_yakit_deposu = float(
    yila_uygun_araclar["yakit_deposu"]
    .dropna()
    .median()
)


st.divider()


# -----------------------------
# İKİ SÜTUN
# -----------------------------

sol, sag = st.columns(2)


with sol:

    konumlar = sorted(
        cars["konum"]
        .dropna()
        .unique()
    )

    konum = st.selectbox(
        "Konum",
        konumlar
    )


    kilometre = st.number_input(
        "Kilometre",
        min_value=0,
        value=100000,
        step=1000
    )


    vitesler = sorted(
        yila_uygun_araclar["vites_tipi"]
        .dropna()
        .unique()
    )

    vites_tipi = st.selectbox(
        "Vites tipi",
        vitesler
    )


    yakitlar = sorted(
        yila_uygun_araclar["yakit_tipi"]
        .dropna()
        .unique()
    )

    yakit_tipi = st.selectbox(
        "Yakıt tipi",
        yakitlar
    )


    kasalar = sorted(
        yila_uygun_araclar["kasa_tipi"]
        .dropna()
        .unique()
    )

    kasa_tipi = st.selectbox(
        "Kasa tipi",
        kasalar
    )


with sag:

    motor_hacmi = st.number_input(
        "Motor hacmi (cc)",
        min_value=0,
        value=varsayilan_motor_hacmi,
        step=1
    )


    motor_gucu = st.number_input(
        "Motor gücü (HP)",
        min_value=0,
        value=varsayilan_motor_gucu,
        step=1
    )


    cekisler = sorted(
        yila_uygun_araclar["cekis"]
        .dropna()
        .unique()
    )

    cekis = st.selectbox(
        "Çekiş tipi",
        cekisler
    )


    ortalama_yakit_tuketimi = st.number_input(
        "Ortalama yakıt tüketimi",
        min_value=0.0,
        value=varsayilan_yakit_tuketimi,
        step=0.1
    )


    yakit_deposu = st.number_input(
        "Yakıt deposu (litre)",
        min_value=0.0,
        value=varsayilan_yakit_deposu,
        step=1.0
    )


    tramer = st.number_input(
        "Tramer tutarı (TL)",
        min_value=0.0,
        value=0.0,
        step=1000.0
    )


# -----------------------------
# HASAR BİLGİLERİ
# -----------------------------

st.subheader("Hasar Bilgileri")

hasar1, hasar2 = st.columns(2)


with hasar1:

    degisen = st.number_input(
        "Değişen parça sayısı",
        min_value=0,
        value=0,
        step=1
    )


with hasar2:

    boyali = st.number_input(
        "Boyalı parça sayısı",
        min_value=0,
        value=0,
        step=1
    )


st.divider()


# -----------------------------
# TAHMİN
# -----------------------------

if st.button(
    "🚘 Fiyat Tahmin Et",
    use_container_width=True
):

    arac_yasi = 2026 - yil
    arac_yasi = max(arac_yasi, 1)

    yillik_km = kilometre / arac_yasi


    if yillik_km > 200000:

        st.warning(
            "Bu aracın yıllık kilometresi eğitim verisindeki "
            "kabul ettiğimiz sınırın üzerinde. "
            "Tahmin daha güvensiz olabilir."
        )


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


    tahmin = model.predict(arac)[0]

    tahmin_formatli = f"{tahmin:,.0f}".replace(",", ".")


    st.success(
        f"### Tahmini Araç Fiyatı: {tahmin_formatli} TL"
    )