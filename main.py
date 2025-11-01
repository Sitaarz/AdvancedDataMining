from config.AppSettings import AppSettings
from src.services.get_data_wrapper import GetDataWrapper
from src.services.movie_data_writer import MovieDataWriter
from src.services.movie_logger import MovieLogger
from src.services.omdb_client import OmdbClient

if __name__ == "__main__":
    AppSettings.load_settings("./config/appsettings.json")

    movie_logger = MovieLogger()
    omdb_client = OmdbClient(AppSettings.api_key)

    with MovieDataWriter() as movie_data_writer:
        try:
            get_data_wrapper = GetDataWrapper(movie_data_writer, movie_logger, omdb_client)
            get_data_wrapper.get_data()
        except Exception as e:
            movie_logger.log_error("Program stopped. Exception appeared: " + str(e))

