from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings  # Ortam değişkenlerini almak için

# Veritabanı bağlantı URL'sini .env dosyasından al
DATABASE_URL = settings.DATABASE_URL

# SQLAlchemy motorunu oluştur
engine = create_engine(DATABASE_URL)

# Veritabanı session yönetimi için session factory oluştur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy model sınıfları için Base tanımı
Base = declarative_base()

# Dependency Injection için bir fonksiyon (FastAPI kullanımı için)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
