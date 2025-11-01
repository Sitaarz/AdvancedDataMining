import unittest
from src.models.domain.movie_data import Movie, Rating
from src.services.movie_data_writer import MovieDataWriter

class TestMovieDataWriter(unittest.TestCase):
    def setUp(self):
        # Używamy bazy "w pamięci" SQLite
        self.writer = MovieDataWriter(":memory:")
        self.writer.__enter__()

    def tearDown(self):
        self.writer.__exit__(None, None, None)

    def test_save_and_get_latest_movie(self):
        movie_1 = Movie(
            Title="Film 1",
            Year="2001",
            Rated="G",
            Released="2001-01-01",
            Runtime="90 min",
            Genre="Drama",
            Director="Jan Kowalski",
            Writer="Anna Nowak",
            Actors="Aktor 1, Aktor 2",
            Plot="Opis filmu",
            Language="Polish",
            Country="Poland",
            Awards="None",
            Poster="",
            Ratings=[Rating(Source="IMDB", Value="7/10", imdbID="ff0000001")],
            Metascore="70",
            imdbRating="7.0",
            imdbVotes="100",
            imdbID="ff0000001",
            Type="movie",
            DVD="2001-01-01",
            BoxOffice="1000000",
            Production="Studio A",
            Website="",
            Response="True"
        )
        movie_2 = Movie(
            Title="Film 2",
            Year="2005",
            Rated="PG",
            Released="2005-01-01",
            Runtime="100 min",
            Genre="Comedy",
            Director="Anna Nowak",
            Writer="Jan Kowalski",
            Actors="Aktor 3, Aktor 4",
            Plot="Opis 2",
            Language="English",
            Country="UK",
            Awards="Oscar",
            Poster="",
            Ratings=[
                Rating(Source="IMDB", Value="8/10", imdbID="ff0000002"),
                Rating(Source="Rotten Tomatoes", Value="95%", imdbID="ff0000002")
            ],
            Metascore="80",
            imdbRating="8.0",
            imdbVotes="200",
            imdbID="ff0000002",
            Type="movie",
            DVD="2005-01-01",
            BoxOffice="5000000",
            Production="Studio B",
            Website="",
            Response="True"
        )
        self.writer.save_movie_entity(movie_1)
        self.writer.save_movie_entity(movie_2)

        latest_id = self.writer.get_latest_movie_id()
        self.assertEqual(latest_id, "ff0000002")

    def test_save_movie_with_ratings(self):
        movie = Movie(
            Title="Test Film",
            Year="2020",
            Rated="PG-13",
            Released="2020-10-10",
            Runtime="120 min",
            Genre="Action",
            Director="Director Test",
            Writer="Writer Test",
            Actors="Actor T",
            Plot="Test plot",
            Language="English",
            Country="USA",
            Awards="None",
            Poster="",
            Ratings=[
                Rating(Source="IMDB", Value="6/10", imdbID="ff0000003"),
                Rating(Source="RT", Value="60%", imdbID="ff0000003")
            ],
            Metascore="60",
            imdbRating="6.0",
            imdbVotes="500",
            imdbID="ff0000003",
            Type="movie",
            DVD="2020-11-10",
            BoxOffice="2000000",
            Production="Test Studio",
            Website="http://example.com",
            Response="True"
        )
        self.writer.save_movie_entity(movie)

        # Sprawdź film w bazie
        self.writer._cursor.execute("SELECT * FROM movies WHERE imdbID=?", (movie.imdbID,))
        row = self.writer._cursor.fetchone()
        self.assertIsNotNone(row)

        # Sprawdź oceny
        self.writer._cursor.execute("SELECT Source, Value FROM ratings WHERE imdbID=?", (movie.imdbID,))
        ratings = self.writer._cursor.fetchall()
        self.assertEqual(len(ratings), 2)
        self.assertIn(("IMDB", "6/10"), ratings)
        self.assertIn(("RT", "60%"), ratings)

    def test_get_latest_movie_no_movies(self):
        result = self.writer.get_latest_movie_id()
        self.assertEqual(result, "ff0000000")

if __name__ == '__main__':
    unittest.main()