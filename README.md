# Paylaşılan Defter (Shared Ledger) Sistemi

Monorepo içindeki uygulamalar için merkezi kredi takip sistemi. Her uygulama için kredi işlemlerini ve bakiyeleri güvenli bir şekilde yönetir.

## Özellikler

- Merkezi kredi yönetimi
- İşlem türleri:
  - DAILY_REWARD: Günlük ödül
  - SIGNUP_CREDIT: Kayıt bonusu
  - CREDIT_SPEND: Kredi harcama
  - CREDIT_ADD: Kredi ekleme
  - CONTENT_CREATION: İçerik oluşturma
  - CONTENT_ACCESS: İçerik erişimi
- Güvenlik kontrolleri:
  - Nonce ile tekrar işlemleri engelleme
  - Yetersiz bakiye kontrolü
  - İşlem türüne göre miktar doğrulama
- Tam test kapsamı
- Migrasyon yönetimi

## Teknik Altyapı

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0
- Pydantic
- PostgreSQL
- Alembic

## Kurulum

1. PostgreSQL veritabanı oluşturun:

bash
createdb shared_ledger

2. Sanal ortam oluşturun ve bağımlılıkları yükleyin:

bash
python -m venv venv
venv\Scripts\activate #MAC: source venv/bin/activate
pip install -r requirements.txt

3. Databese adresinizi girin:

DATABASE_URL=postgresql://postgres:youradress..

4. Migrasyonları çalıştırın:

bash
alembic upgrade head

5. Uygulamayı başlatın:

bash
uvicorn app.main:app --reload

6. POSTGRESQL'i projeye bağlayın:

psql -U postgres -d shared_ledger

7. POSTGRESQL tablo kontrolü yapın(POSTGRESQL'i projeye bağlayın sonra yapın):

bash
\dt

8. FastAPI'nin çalıştığını kontrol edin:

bash
curl http://localhost:8000/docs

GET-POST işlemlerini kontrol edin.

9. Testleri çalıştırın:

bash
pytest

DİP NOT: BÜTÜN İŞLEMLERİ YAPMADAN ÖNCE SANAL ORTAMIN AKTİF OLDUĞUNDAN EMİN OLUNUZ.
