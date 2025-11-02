from config.AppSettings import AppSettings
from src.services.get_data_wrapper import GetDataWrapper
from src.services.movie_data_writer import MovieDataWriter
from src.services.movie_logger import MovieLogger
from src.services.omdb_client import OmdbClient

if __name__ == "__main__":
    AppSettings.load_settings("./config/appsettings.json")
    movie_logger = MovieLogger()

    apiKey = AppSettings.api_key
    if apiKey is None or apiKey == "":
        movie_logger.log_error("API key is not set. Raising error.")
        raise ValueError("API key is not set. Go to config/appsettings.json and set your API key.")

    omdb_client = OmdbClient(apiKey)

    with MovieDataWriter() as movie_data_writer:
        try:
            get_data_wrapper = GetDataWrapper(movie_data_writer, movie_logger, omdb_client)
            get_data_wrapper.get_data()
        except Exception as e:
            movie_logger.log_error("Program stopped. Exception appeared: " + str(e))
            raise

