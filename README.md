# Netflix Öneri Sistemi 

Bu proje, bir film öneri sistemi geliştirmek için **FastAPI**, **SQLAlchemy** ve **KMeans** algoritmasını kullanır. Kullanıcıların izleme geçmişine ve film özelliklerine dayalı olarak öneriler sunar.

## Özellikler
- Kullanıcılar ve filmler için veritabanı yönetimi.
- Kullanıcıların izleme geçmişine dayalı film önerileri.
- KMeans algoritması ile film kümeleri oluşturma.
- FastAPI ile RESTful API uç noktaları.

## Gereksinimler
Bu projeyi çalıştırmak için aşağıdaki yazılımlara ihtiyacınız var:
- Python 3.9 veya üzeri
- PostgreSQL veritabanı

## Kurulum
1. **Depoyu klonlayın:**
   ```bash
   git clone https://github.com/ilknuraycacicekk/proje_adı.git
   cd proje_adı
   ```

2. **Gerekli kütüphaneleri yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

3. **PostgreSQL veritabanını oluşturun:**
   PostgreSQL'de bir veritabanı oluşturun:
   ```sql
   CREATE DATABASE netflix;
   ```

4. **Veritabanı bağlantısını yapılandırın:**
   `database.py` dosyasındaki `DATABASE_URL` değişkenini kendi PostgreSQL bağlantı bilgilerinizle güncelleyin:
   ```python
   DATABASE_URL = "postgresql://<kullanıcı_adı>:<şifre>@localhost:5432/netflix"
   ```

5. **Veritabanı tablolarını oluşturun ve örnek verileri ekleyin:**
   ```bash
   python database.py
   ```

6. **API'yi başlatın:**
   ```bash
   uvicorn api:app --reload
   ```

7. **API'yi test edin:**
   Tarayıcınızda şu URL'yi açarak API uç noktalarını test edebilirsiniz:
   - Swagger Dokümantasyonu: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Uç Noktaları
### 1. **Film Önerisi Al (`GET /recommendations/{user_id}`)**
   - **Açıklama:** Belirli bir kullanıcı için film önerileri döndürür.
   - **Parametreler:**
     - `user_id` (int): Kullanıcının ID'si.
     - `limit` (int, opsiyonel): Döndürülecek öneri sayısı (varsayılan: 5).
   - **Örnek İstek:**
     ```bash
     curl -X GET "http://127.0.0.1:8000/recommendations/1?limit=5"
     ```
   - **Örnek Yanıt:**
     ```json
     {
       "recommendations": [
         {"title": "Aksiyon Filmi", "genre": "Aksiyon", "rating": 8.5},
         {"title": "Komedi Filmi", "genre": "Komedi", "rating": 7.2}
       ]
     }
     ```

## Proje Yapısı
```plaintext
.
├── api.py             # FastAPI uygulaması
├── database.py        # Veritabanı tabloları ve örnek veri ekleme
├── model.py           # KMeans modeli ve öneri sistemi
├── requirements.txt   # Gerekli Python kütüphaneleri
└── README.md          # Proje açıklaması
```

## Katkıda Bulunma
Katkıda bulunmak isterseniz, lütfen bir **pull request** gönderin veya bir **issue** açın.

## Lisans
Bu proje MIT Lisansı ile lisanslanmıştır.
