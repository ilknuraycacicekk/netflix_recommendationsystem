from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import random

# PostgreSQL bağlantı bilgileri
DATABASE_URL = "postgresql://postgres:abcde@localhost:5432/netflix"

# SQLAlchemy ayarları
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Kullanıcı tablosu
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    preferences = Column(String)  # Kullanıcının tercihleri (ör. türler)

# Film tablosu
class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)
    rating = Column(Float)
    release_year = Column(Integer)  # Yayın yılı

# Film puanlama tablosu
class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    rating = Column(Float)

# İzleme geçmişi tablosu
class WatchHistory(Base):
    __tablename__ = "watch_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    user = relationship("User", back_populates="watch_history")
    movie = relationship("Movie", back_populates="watch_history")

User.watch_history = relationship("WatchHistory", back_populates="user")
Movie.watch_history = relationship("WatchHistory", back_populates="movie")

# Veritabanını oluştur
def init_db():
    Base.metadata.create_all(bind=engine)

# Örnek veri ekleme
def populate_data():
    session = SessionLocal()
    try:
        # 100 Kullanıcı oluştur
        users = [
            User(
                name=f"Kullanıcı {i}",
                age=random.randint(18, 60),
                preferences=random.choice(["Aksiyon,Komedi", "Dram,Romantik", "Gerilim,Korku", "Bilim Kurgu,Fantastik"])
            )
            for i in range(1, 101)
        ]
        session.add_all(users)

        # Filmler
        movies = [
            Movie(title="Aksiyon Filmi 1", genre="Aksiyon", rating=8.5, release_year=2023),
            Movie(title="Komedi Filmi 1", genre="Komedi", rating=7.2, release_year=2021),
            Movie(title="Dram Filmi 1", genre="Dram", rating=9.0, release_year=2020),
            Movie(title="Korku Filmi 1", genre="Korku", rating=6.8, release_year=2019),
            Movie(title="Bilim Kurgu Filmi 1", genre="Bilim Kurgu", rating=8.9, release_year=2022),
            Movie(title="Fantastik Filmi 1", genre="Fantastik", rating=8.3, release_year=2020),
        ]
        session.add_all(movies)

        # İzleme geçmişi
        watch_history = [
            WatchHistory(user_id=random.randint(1, 100), movie_id=random.randint(1, len(movies)))
            for _ in range(200)  # 200 izleme geçmişi kaydı
        ]
        session.add_all(watch_history)

        # Veritabanına kaydet
        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
    populate_data()