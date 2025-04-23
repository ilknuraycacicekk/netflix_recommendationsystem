import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session
from database import Movie, Rating, WatchHistory

class MovieRecommender:
    def __init__(self, n_clusters=5):
        """
        Film öneri sistemi için KMeans modeli.
        - **n_clusters**: KMeans modeli için küme sayısı (varsayılan: 5)
        """
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()
        self.movie_features = None
        self.movie_clusters = None

    def prepare_features(self, db: Session):
        """
        Filmler için özellikleri hazırlar.
        - **db**: SQLAlchemy oturumu
        """
        movies = db.query(Movie).all()
        if not movies:
            raise ValueError("Veritabanında film bulunamadı.")

        ratings = db.query(Rating).all()
        watch_history = db.query(WatchHistory).all()

        features = []
        for movie in movies:
            # Kullanıcı puanlamaları
            movie_ratings = [r.rating for r in ratings if r.movie_id == movie.id]
            avg_rating = np.mean(movie_ratings) if movie_ratings else 0

            # İzlenme sayısı
            watch_count = len([w for w in watch_history if w.movie_id == movie.id])

            # Film özellikleri
            features.append([
                movie.rating or 0,  # IMDB puanı
                avg_rating,         # Kullanıcı puanlamaları ortalaması
                watch_count,        # İzlenme sayısı
                movie.release_year or 0  # Yayın yılı (None ise 0 olarak ele alınır)
            ])

        self.movie_features = np.array(features)
        return self.movie_features

    def fit(self, db: Session):
        """
        KMeans modelini eğitir.
        - **db**: SQLAlchemy oturumu
        """
        features = self.prepare_features(db)
        if features.size == 0:
            raise ValueError("Model eğitimi için yeterli veri yok.")

        # Küme sayısını veritabanındaki film sayısına göre ayarla
        n_samples = features.shape[0]
        if n_samples < self.n_clusters:
            self.n_clusters = n_samples

        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        scaled_features = self.scaler.fit_transform(features)
        self.kmeans.fit(scaled_features)
        self.movie_clusters = self.kmeans.labels_
        return self

    def get_recommendations(self, db: Session, user_id: int, n_recommendations: int = 5):
        """
        Kullanıcı için film önerileri döndürür.
        - **db**: SQLAlchemy oturumu
        - **user_id**: Kullanıcının ID'si
        - **n_recommendations**: Döndürülecek öneri sayısı (varsayılan: 5)
        """
        # Kullanıcının izlediği filmleri bul
        user_watched = db.query(WatchHistory.movie_id).filter(WatchHistory.user_id == user_id).all()
        watched_movie_ids = [w[0] for w in user_watched]

        if not watched_movie_ids:
            # Kullanıcı hiç film izlememişse en yüksek puanlı filmleri öner
            return db.query(Movie).order_by(Movie.rating.desc()).limit(n_recommendations).all()

        # İzlenen filmlerin kümelerini bul
        watched_clusters = [self.movie_clusters[movie_id - 1] for movie_id in watched_movie_ids]

        # En çok izlenen küme
        most_watched_cluster = max(set(watched_clusters), key=watched_clusters.count)

        # Aynı kümedeki izlenmemiş filmleri öner
        recommendations = []
        for i, cluster in enumerate(self.movie_clusters):
            movie_id = i + 1
            if cluster == most_watched_cluster and movie_id not in watched_movie_ids:
                movie = db.query(Movie).filter(Movie.id == movie_id).first()
                if movie:
                    recommendations.append(movie)
                    if len(recommendations) >= n_recommendations:
                        break

        return recommendations