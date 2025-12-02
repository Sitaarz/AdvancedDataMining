import unittest

from config.AppSettings import AppSettings
from src.DataDownload.services import OmdbClient


class OmdbClientTests(unittest.TestCase):
    def setUp(self):
        AppSettings.load_settings("../../config/appsettings.json")
        self.omdb_client = OmdbClient(AppSettings.api_key)

    def test_get_movie_by_id(self):
        movie = {
            "Title": "Star Wars: Episode IV - A New Hope",
            "Year": "1977",
            "Rated": "PG",
            "Released": "25 May 1977",
            "Runtime": "121 min",
            "Genre": "Action, Adventure, Fantasy",
            "Director": "George Lucas",
            "Writer": "George Lucas",
            "Actors": "Mark Hamill, Harrison Ford, Carrie Fisher",
            "Plot": "The Imperial Forces, under orders from cruel Darth Vader, hold Princess Leia hostage in their efforts to quell the rebellion against the Galactic Empire. Luke Skywalker and Han Solo, captain of the Millennium Falcon, work together with the companionable droid duo R2-D2 and C-3PO to rescue the beautiful princess, help the Rebel Alliance and restore freedom and justice to the Galaxy.",
            "Language": "English",
            "Country": "United States",
            "Awards": "Won 6 Oscars. 70 wins & 31 nominations total",
            "Poster": "https://m.media-amazon.com/images/M/MV5BOGUwMDk0Y2MtNjBlNi00NmRiLTk2MWYtMGMyMDlhYmI4ZDBjXkEyXkFqcGc@._V1_SX300.jpg",
            "Ratings": [
                {"Source": "Internet Movie Database", "Value": "8.6/10"},
                {"Source": "Rotten Tomatoes", "Value": "94%"},
                {"Source": "Metacritic", "Value": "90/100"}
            ],
            "Metascore": "90",
            "imdbRating": "8.6",
            "imdbVotes": "1,536,348",
            "imdbID": "tt0076759",
            "Type": "movie",
            "DVD": "N/A",
            "BoxOffice": "$460,998,507",
            "Production": "N/A",
            "Website": "N/A",
            "Response": "True"
        }

        result = self.omdb_client.get_film_by_id("tt0076759")
        self.assertEqual(result.json(), movie)

if __name__ == "__main__":
    unittest.main()