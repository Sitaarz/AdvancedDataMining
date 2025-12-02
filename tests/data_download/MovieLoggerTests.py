import unittest
from unittest.mock import patch, MagicMock

from src.DataDownload.services import MovieLogger


class TestMovieLogger(unittest.TestCase):

    @patch('logging.getLogger')
    def test_log_info(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        logger = MovieLogger(log_file='../test.log')
        logger.log_info('Informacja testowa')

        mock_logger.info.assert_called_with('Informacja testowa')

    @patch('logging.getLogger')
    def test_log_error(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        logger = MovieLogger(log_file='../test.log')
        logger.log_error('Błąd testowy')

        mock_logger.error.assert_called_with('Błąd testowy')


if __name__ == '__main__':
    unittest.main()