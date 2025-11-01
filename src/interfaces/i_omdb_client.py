import abc

from requests import Response

from src.models.dto.movie_data_dto import MovieDTO


class IOmdbClient(abc.ABC):
    @abc.abstractmethod
    def get_film_by_id(self, imdb_id: str) -> Response:
        pass
