from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, User, Movie
from model import MovieRecommender

app = FastAPI()
recommender = MovieRecommender()

# Veritabanı bağlantısı
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Kullanıcı ekleme
@app.post("/users/", summary="Yeni bir kullanıcı ekle")
def create_user(name: str, age: int, preferences: str, db: Session = Depends(get_db)):
    """
    Yeni bir kullanıcı ekler.

    - **name**: Kullanıcının adı
    - **age**: Kullanıcının yaşı
    - **preferences**: Kullanıcının tercih ettiği türler (ör. "Aksiyon,Komedi")
    """
    existing_user = db.query(User).filter(User.name == name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Bu isimde bir kullanıcı zaten mevcut.")
    user = User(name=name, age=age, preferences=preferences)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Film ekleme
@app.post("/movies/", summary="Yeni bir film ekle")
def create_movie(title: str, genre: str, rating: float, release_year: int, db: Session = Depends(get_db)):
    """
    Yeni bir film ekler.

    - **title**: Filmin adı
    - **genre**: Filmin türü (ör. "Aksiyon")
    - **rating**: Filmin puanı (ör. 8.5)
    - **release_year**: Filmin yayın yılı
    """
    existing_movie = db.query(Movie).filter(Movie.title == title).first()
    if existing_movie:
        raise HTTPException(status_code=400, detail="Bu isimde bir film zaten mevcut.")
    movie = Movie(title=title, genre=genre, rating=rating, release_year=release_year)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

# Öneri yapma
@app.get("/recommendations/{user_id}", summary="Kullanıcı için film önerileri al")
def get_recommendations(user_id: int, limit: int = 5, db: Session = Depends(get_db)):
    """
    Kullanıcı için film önerileri döndürür.

    - **user_id**: Kullanıcının ID'si
    - **limit**: Döndürülecek maksimum öneri sayısı (varsayılan: 5)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    try:
        recommender.fit(db)
        recommendations = recommender.get_recommendations(db, user_id)
        limited_recommendations = recommendations[:limit]
        return {
            "recommendations": [
                {"title": movie.title, "genre": movie.genre, "rating": movie.rating}
                for movie in limited_recommendations
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))