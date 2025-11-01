import sqlite3
from dataclasses import asdict

from src.interfaces.i_movie_data_writer import IMovieDataWriter
from src.models.domain.movie_data import Movie, Rating


class MovieDataWriter(IMovieDataWriter):
    def __init__(self, db_file="movies.db"):
        self.db_file = db_file
        self._conn = None
        self._cursor = None
        self._number_of_movies_to_save = 0

    def __enter__(self):
        self._conn = sqlite3.connect(self.db_file)
        self._cursor = self._conn.cursor()
        self._initialize_database()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            self._conn.commit()
            self._cursor.close()
            self._conn.close()

    def _initialize_database(self):
        self._cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            imdbID TEXT PRIMARY KEY,
            Title TEXT,
            Year TEXT,
            Rated TEXT,
            Released TEXT,
            Runtime TEXT,
            Genre TEXT,
            Director TEXT,
            Writer TEXT,
            Actors TEXT,
            Plot TEXT,
            Language TEXT,
            Country TEXT,
            Awards TEXT,
            Poster TEXT,
            Metascore TEXT,
            imdbRating TEXT,
            imdbVotes TEXT,
            Type TEXT,
            DVD TEXT,
            BoxOffice TEXT,
            Production TEXT,
            Website TEXT,
            Response TEXT,
            Error TEXT,
            FOREIGN KEY(Genre) REFERENCES genres(genre),
            FOREIGN KEY(Actors) REFERENCES actors(actor)       
        );
        """)
        self._cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imdbID TEXT,
            Source TEXT,
            Value TEXT,
            FOREIGN KEY(imdbID) REFERENCES movies(imdbID)
        );
        """)

        self._cursor.execute("CREATE  TABLE IF NOT EXISTS genres (genre TEXT PRIMARY KEY)")

        self._cursor.execute("CREATE TABLE IF NOT EXISTS actors (actor TEXT PRIMARY KEY)")

    def save_movie_entity(self, movie: Movie) -> None:
        movie_dict = asdict(movie)
        del movie_dict['Ratings']
        del movie_dict['Actors']
        del movie_dict['Genre']

        columns = ', '.join(list(movie_dict.keys()))
        placeholders = ', '.join(['?'] * len(movie_dict.keys()))
        values = tuple(movie_dict.values())

        if len(movie.Genre) > 0 or len(movie.Actors) > 0:
            for genre in movie.Genre:
                self._cursor.execute("INSERT OR IGNORE INTO genres (genre) VALUES (?)", (genre,))
                for actor in movie.Actors:
                    self._cursor.execute("INSERT OR IGNORE INTO actors (actor) VALUES (?)", (actor,))
                    self._cursor.execute(f"INSERT OR REPLACE INTO movies ({columns}, genre, actors) VALUES ({placeholders}, ?, ?)", values + (genre, actor))


        self._cursor.execute(f"INSERT OR REPLACE INTO movies ({columns}) VALUES ({placeholders})", values)

        ratings = movie.Ratings
        self._cursor.execute("DELETE FROM ratings WHERE imdbID=?", (movie.imdbID,))

        if len(ratings) > 0:

            for rating in ratings:
                rating_columns = ', '.join(list(asdict(rating).keys()))
                rating_placeholders = ', '.join(['?'] * len(asdict(rating)))
                rating_values = tuple((asdict(rating).values()))
                self._cursor.execute(
                    f"INSERT INTO ratings ({rating_columns}) VALUES ({rating_placeholders})",
                    tuple(asdict(rating).values())
                )
        self._number_of_movies_to_save += 1
        if self._number_of_movies_to_save >= 1000:
            self._conn.commit()
            self._number_of_movies_to_save = 0


    def get_latest_movie_id(self) -> str:
        self._cursor.execute("SELECT imdbID FROM movies ORDER BY imdbID DESC LIMIT 1")
        one = self._cursor.fetchone()
        return one[0] if one is not None else "tt0000000"

