import unittest
from unittest.mock import Mock, patch
from argparse import ArgumentError
from src.services.get_data_wrapper import GetDataWrapper


class TestGetDataWrapper(unittest.TestCase):

    def setUp(self):
        self.mock_writer = Mock()
        self.mock_logger = Mock()
        self.mock_client = Mock()

        self.wrapper = GetDataWrapper(
            movie_data_writer=self.mock_writer,
            movie_logger=self.mock_logger,
            omdb_client=self.mock_client
        )

    def test_increase_omdb_movie_id_happy_path(self):
        result = self.wrapper.increase_omdb_movie_id("tt0000001")
        self.assertEqual(result, "tt0000002")

    def test_increase_omdb_movie_id_invalid_prefix(self):
        with self.assertRaises(ValueError):
            self.wrapper.increase_omdb_movie_id("ff0000001")

    def test_increase_omdb_movie_id_none(self):
        with self.assertRaises(ValueError):
            self.wrapper.increase_omdb_movie_id(None)

    @patch("src.services.get_data_wrapper.MovieDTO")
    def test_get_single_entity_movie_found(self, mock_movie_dto):
        movie_id = "tt0000001"
        # Setup: Mock odpowiedzi klienta OMDB
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "val"}

        mock_movie = Mock()
        mock_movie.Response = "True"
        mock_movie.imdbID = movie_id

        # Mockowanie DTO (from_dict i to_domain)
        mock_movie_dto.from_dict.return_value = mock_movie_dto
        mock_movie_dto.to_domain.return_value = mock_movie

        self.mock_client.get_film_by_id.return_value = mock_response

        self.wrapper.get_single_entity(movie_id)

        self.mock_writer.save_movie_entity.assert_called_once_with(mock_movie)
        self.mock_logger.log_info.assert_called_with(f"Movie with id {movie_id} saved successfully.")

    @patch("src.services.get_data_wrapper.MovieDTO")
    def test_get_single_entity_movie_not_found(self, mock_movie_dto):
        movie_id = "tt0000009"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}

        mock_movie = Mock()
        mock_movie.Response = "False"
        mock_movie.imdbID = movie_id

        mock_movie_dto.from_dict.return_value = mock_movie_dto
        mock_movie_dto.to_domain.return_value = mock_movie

        self.mock_client.get_film_by_id.return_value = mock_response

        self.wrapper.get_single_entity(movie_id)

        self.mock_writer.save_movie_entity.assert_called_once_with(mock_movie)
        self.mock_logger.log_error.assert_called()  # Zostanie wywołany error log

    def test_get_single_entity_api_failure(self):
        movie_id = "tt9999999"
        # Odpowiedź z błędem zawsze -> po 3 próbach rzucany wyjątek
        mock_response = Mock()
        mock_response.status_code = 500
        self.mock_client.get_film_by_id.return_value = mock_response

        with self.assertRaises(ConnectionError):
            self.wrapper.get_single_entity(movie_id)
        self.mock_logger.log_error.assert_called_with("Connection with OMDB API failed. Terminationg download")


if __name__ == '__main__':
    unittest.main()