import abc

from requests import Response


class IOmdbClient(abc.ABC):
    @abc.abstractmethod
    def get_film_by_id(self, imdb_id: str) -> Response:
        pass
