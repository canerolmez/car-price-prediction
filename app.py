import streamlit as st
import pandas as pd
import joblib


# --------------------------------------------------
# SAYFA AYARLARI
# --------------------------------------------------

st.set_page_config(
    page_title="Araç Fiyat Tahmini",
    page_icon="🚗",
    layout="wide"
)


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        opacity: 0.75;
        margin-bottom: 35px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 600;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    .result-card {
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 18px;
        padding: 30px;
        text-align: center;
        margin-top: 25px;
        background: rgba(255,255,255,0.04);
    }

    .result-label {
        font-size: 16px;
        opacity: 0.7;
        margin-bottom: 8px;
    }

    .result-price {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .result-note {
        font-size: 14px;
        opacity: 0.65;
    }

    div.stButton > button {
        height: 55px;
        font-size: 18px;
        font-weight: 600;
        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# MODEL VE VERİ
# --------------------------------------------------

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


# --------------------------------------------------
# BAŞLIK
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🚗 Araç Fiyat Tahmini</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Araç özelliklerini seçin, makine öğrenmesi modeli tahmini piyasa değerini hesaplasın.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# ARAÇ SEÇİMİ
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Araç Seçimi</div>',
    unsafe_allow_html=True
)


markalar = sorted(
    cars["marka"]
    .dropna()
    .unique()
)


secim1, secim2, secim3, secim4 = st.columns(4)


with secim1:

    marka = st.selectbox(
        "Marka",
        markalar
    )


seriler = sorted(
    cars[
        cars["marka"] == marka
    ]["seri"]
    .dropna()
    .unique()
)


with secim2:

    seri = st.selectbox(
        "Seri",
        seriler
    )


modeller = sorted(
    cars[
        (cars["marka"] == marka) &
        (cars["seri"] == seri)
    ]["model"]
    .dropna()
    .unique()
)


with secim3:

    model_adi = st.selectbox(
        "Model",
        modeller
    )


uygun_araclar = cars[
    (cars["marka"] == marka) &
    (cars["seri"] == seri) &
    (cars["model"] == model_adi)
]


yillar = sorted(
    uygun_araclar["yil"]
    .dropna()
    .astype(int)
    .unique(),
    reverse=True
)


with secim4:

    yil = st.selectbox(
        "Yıl",
        yillar
    )


yila_uygun_araclar = uygun_araclar[
    uygun_araclar["yil"] == yil
]


# --------------------------------------------------
# GÜVENLİ MEDYAN FONKSİYONU
# --------------------------------------------------

def guvenli_medyan(
    dataframe,
    kolon,
    varsayilan
):

    medyan = (
        dataframe[kolon]
        .dropna()
        .median()
    )

    if pd.isna(medyan):
        return varsayilan

    return medyan


varsayilan_motor_hacmi = int(
    guvenli_medyan(
        yila_uygun_araclar,
        "motor_hacmi",
        1500
    )
)

varsayilan_motor_gucu = int(
    guvenli_medyan(
        yila_uygun_araclar,
        "motor_gucu",
        100
    )
)

varsayilan_yakit_tuketimi = float(
    guvenli_medyan(
        yila_uygun_araclar,
        "ortalama_yakit_tuketimi",
        5.0
    )
)

varsayilan_yakit_deposu = float(
    guvenli_medyan(
        yila_uygun_araclar,
        "yakit_deposu",
        50.0
    )
)


st.divider()


# --------------------------------------------------
# KULLANIM BİLGİLERİ
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Kullanım Bilgileri</div>',
    unsafe_allow_html=True
)


kullanim1, kullanim2, kullanim3 = st.columns(3)


with kullanim1:

    konumlar = sorted(
        cars["konum"]
        .dropna()
        .unique()
    )

    konum = st.selectbox(
        "Konum",
        konumlar
    )


with kullanim2:

    kilometre = st.number_input(
        "Kilometre",
        min_value=0,
        value=100000,
        step=1000
    )


with kullanim3:

    tramer = st.number_input(
        "Tramer Tutarı (TL)",
        min_value=0.0,
        value=0.0,
        step=1000.0
    )


# --------------------------------------------------
# TEKNİK BİLGİLER
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Teknik Bilgiler</div>',
    unsafe_allow_html=True
)


vitesler = sorted(
    yila_uygun_araclar["vites_tipi"]
    .dropna()
    .unique()
)

yakitlar = sorted(
    yila_uygun_araclar["yakit_tipi"]
    .dropna()
    .unique()
)

kasalar = sorted(
    yila_uygun_araclar["kasa_tipi"]
    .dropna()
    .unique()
)

cekisler = sorted(
    yila_uygun_araclar["cekis"]
    .dropna()
    .unique()
)


teknik1, teknik2, teknik3 = st.columns(3)


with teknik1:

    vites_tipi = st.selectbox(
        "Vites Tipi",
        vitesler
    )

    motor_hacmi = st.number_input(
        "Motor Hacmi (cc)",
        min_value=0,
        value=varsayilan_motor_hacmi,
        step=1
    )


with teknik2:

    yakit_tipi = st.selectbox(
        "Yakıt Tipi",
        yakitlar
    )

    motor_gucu = st.number_input(
        "Motor Gücü (HP)",
        min_value=0,
        value=varsayilan_motor_gucu,
        step=1
    )


with teknik3:

    kasa_tipi = st.selectbox(
        "Kasa Tipi",
        kasalar
    )

    cekis = st.selectbox(
        "Çekiş Tipi",
        cekisler
    )


teknik4, teknik5 = st.columns(2)


with teknik4:

    ortalama_yakit_tuketimi = st.number_input(
        "Ortalama Yakıt Tüketimi",
        min_value=0.0,
        value=varsayilan_yakit_tuketimi,
        step=0.1
    )


with teknik5:

    yakit_deposu = st.number_input(
        "Yakıt Deposu (Litre)",
        min_value=0.0,
        value=varsayilan_yakit_deposu,
        step=1.0
    )


# --------------------------------------------------
# HASAR
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Hasar Bilgileri</div>',
    unsafe_allow_html=True
)


hasar1, hasar2 = st.columns(2)


with hasar1:

    degisen = st.number_input(
        "Değişen Parça Sayısı",
        min_value=0,
        value=0,
        step=1
    )


with hasar2:

    boyali = st.number_input(
        "Boyalı Parça Sayısı",
        min_value=0,
        value=0,
        step=1
    )


st.write("")
st.write("")


# --------------------------------------------------
# TAHMİN
# --------------------------------------------------

if st.button(
    "🚘 Fiyatı Tahmin Et",
    use_container_width=True,
    type="primary"
):

    arac_yasi = max(
        2026 - yil,
        1
    )

    yillik_km = kilometre / arac_yasi


    if yillik_km > 200000:

        st.warning(
            "Bu aracın yıllık kilometresi eğitim verisindeki "
            "sınırın üzerinde. Tahmin daha az güvenilir olabilir."
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

    tahmin_formatli = (
        f"{tahmin:,.0f}"
        .replace(",", ".")
    )


    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-label">
                Tahmini Araç Değeri
            </div>

            <div class="result-price">
                {tahmin_formatli} TL
            </div>

            <div class="result-note">
                Tahmin makine öğrenmesi modeli tarafından üretilmiştir.
                Gerçek piyasa değeri araç kondisyonu ve piyasa koşullarına göre değişebilir.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )