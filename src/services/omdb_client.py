import requests
from requests import Response

from src.interfaces.i_omdb_client import IOmdbClient
from src.models.dto.movie_data_dto import MovieDTO


class OmdbClient(IOmdbClient):
    def __init__(self, api_key: str):
        self.base_url = "http://www.omdbapi.com"
        self.api_key = api_key

    # IMDB ids info:
    # tt0050083 is the unique identifier for the movie "12 Angry Men (1957)",
    # where tt signifies that it's a title entity and 0050083 uniquely indicates "12 Angry Men (1957)".
    def get_film_by_id(self, imdb_id: str) -> Response:
        response = requests.get(self.base_url + f"?apikey={self.api_key}&i={imdb_id}&plot=full")
        return response
