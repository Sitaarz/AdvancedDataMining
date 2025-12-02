from config.AppSettings import AppSettings
from src.DataDownload.services import MovieDataWriter
from src.DataDownload.services import MovieLogger
from src.DataDownload.services import OmdbClient
from src.DataDownload.services.get_data_wrapper import GetDataWrapper

if __name__ == "__main__":
    AppSettings.load_settings("../config/appsettings.json")
    movie_logger = MovieLogger()

    apiKey = AppSettings.api_key
    if apiKey is None or apiKey == "":
        movie_logger.log_error("API key is not set. Raising error.")
        raise ValueError("API key is not set. Go to config/appsettings.json and set your API key.")

    omdb_client = OmdbClient(apiKey)

    with MovieDataWriter() as movie_data_writer:
        get_data_wrapper = GetDataWrapper(movie_data_writer, movie_logger, omdb_client)
        while True:
            trial_number = 1
            try:
                get_data_wrapper.get_data()
            except Exception as e:
                movie_logger.log_error("Exception appeared: " + str(e))

