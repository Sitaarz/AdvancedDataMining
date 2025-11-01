import time

from config.AppSettings import AppSettings
from src.interfaces.i_movie_logger import IMovieLogger
from src.interfaces.i_movie_data_writer import IMovieDataWriter
from src.interfaces.i_omdb_client import IOmdbClient
from src.models.dto.movie_data_dto import MovieDTO


class GetDataWrapper():
    def __init__(self,
                 movie_data_writer: IMovieDataWriter,
                 movie_logger: IMovieLogger,
                 omdb_client: IOmdbClient):
        self._movie_data_writer = movie_data_writer
        self._movie_logger = movie_logger
        self._omdb_client = omdb_client

    def get_data(self) -> None:
        latest_movie_id = self._movie_data_writer.get_latest_movie_id() if AppSettings.start_from_id is None else AppSettings.start_from_id
        while True:
            if AppSettings.stop_at_id is not None and latest_movie_id == AppSettings.stop_at_id:
                break
            self.get_single_entity(latest_movie_id)
            latest_movie_id = self.increase_omdb_movie_id(latest_movie_id)


    def get_single_entity(self, movie_id: str) -> None:
        movie_response = self._omdb_client.get_film_by_id(movie_id)
        trials = 1
        while trials < 3:
            if movie_response.status_code == 200:
                movie_response_json = movie_response.json()
                movie_response_json["imdbID"] = movie_id
                movie_dto = MovieDTO.from_dict(movie_response_json)
                movie_domain = movie_dto.to_domain()

                self._movie_data_writer.save_movie_entity(movie_domain)

                if movie_domain.Response != "True":
                    self._movie_logger.log_error(f"Movie with id {movie_domain.imdbID} not found. Saving empty result. Response: {movie_domain.Response}")
                else:
                    self._movie_logger.log_info(f"Movie with id {movie_domain.imdbID} saved successfully.")
                return
            trials += 1
            time.sleep(trials**2)
        self._movie_logger.log_error("Connection with OMDB API failed. Terminationg download")
        raise ConnectionError("Connection with OMDB API failed. Terminationg download")

    def increase_omdb_movie_id(self, movie_id: str) -> str:
        if movie_id is None:
            raise ValueError("Movie id is none")

        if movie_id[:2] != "tt":
            raise ValueError("Movie id is not valid")

        movie_id_int = int(movie_id[2:])
        movie_id_int += 1
        movie_id_int_str = str(movie_id_int)
        movie_id_int_str = "tt" + movie_id_int_str.zfill(7)
        return movie_id_int_str

