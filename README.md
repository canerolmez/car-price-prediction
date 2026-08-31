# Car Price Prediction

Makine öğrenmesi kullanarak araç özelliklerinden tahmini araç fiyatı üreten bir web uygulaması.

## Proje Özeti

Bu projede araçlara ait çeşitli özellikler kullanılarak bir regresyon modeli eğitildi.

Kullanıcı web arayüzünden araç bilgilerini seçerek tahmini araç fiyatını görüntüleyebilir.

## Kullanılan Teknolojiler

- Python
- Pandas
- Scikit-learn
- Random Forest Regressor
- Streamlit
- Joblib
- Git / GitHub

## Kullanılan Özellikler

Model aşağıdaki araç özelliklerini kullanır:

- Marka
- Seri
- Model
- Yıl
- Kilometre
- Konum
- Vites tipi
- Yakıt tipi
- Kasa tipi
- Motor hacmi
- Motor gücü
- Çekiş tipi
- Ortalama yakıt tüketimi
- Yakıt deposu
- Tramer
- Değişen parça sayısı
- Boyalı parça sayısı

Ek olarak:

- Araç yaşı
- Yıllık kilometre

özellikleri veri üzerinden oluşturulmuştur.

## Model

Model olarak `RandomForestRegressor` kullanılmıştır.

Veri:

- Eğitim verisi: %80
- Test verisi: %20

olarak ayrılmıştır.

### Test Sonuçları

Yaklaşık olarak:

- MAE: 63.662 TL
- RMSE: 99.500 TL
- R²: 0.955

R² değeri bir doğruluk yüzdesi değildir. Modelin test verisindeki fiyat değişkenliğinin ne kadarını açıklayabildiğini gösterir.

## Web Arayüzü

Streamlit ile geliştirilen arayüzde kullanıcı:

1. Marka
2. Seri
3. Model
4. Yıl
5. Teknik özellikler
6. Kilometre ve konum
7. Hasar bilgileri

gibi bilgileri girerek tahmini araç fiyatını görüntüleyebilir.

Dropdown seçenekleri veri setindeki gerçek araç bilgilerine göre dinamik olarak filtrelenmektedir.

## Projeyi Çalıştırma

Sanal ortamı aktifleştirin:

```bash
source .venv/Scripts/activate