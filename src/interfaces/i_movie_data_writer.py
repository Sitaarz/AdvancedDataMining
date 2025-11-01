import abc

from src.models.domain.movie_data import Movie


class IMovieDataWriter(abc.ABC):
    @abc.abstractmethod
    def __enter__(self):
        pass
    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    @abc.abstractmethod
    def save_movie_entity(self, movie: Movie, ratings: list):
        pass
    @abc.abstractmethod
    def get_latest_movie_id(self):
        pass
