from dataclasses import dataclass, asdict, field
from typing import List, Optional

from src.DataDownload.models.domain.movie_data import Movie, Rating


@dataclass
class MovieDTO:
    Title: Optional[str] = None
    Year: Optional[str] = None
    Rated: Optional[str] = None
    Released: Optional[str] = None
    Runtime: Optional[str] = None
    Genre: List[str] = field(default_factory=list)
    Director: Optional[str] = None
    Writer: Optional[str] = None
    Actors: List[str] = field(default_factory=list)
    Plot: Optional[str] = None
    Language: Optional[str] = None
    Country: Optional[str] = None
    Awards: Optional[str] = None
    Poster: Optional[str] = None
    Ratings: List[dict] = field(default_factory=list)
    Metascore: Optional[str] = None
    imdbRating: Optional[str] = None
    imdbVotes: Optional[str] = None
    imdbID: Optional[str] = None
    Type: Optional[str] = None
    DVD: Optional[str] = None
    BoxOffice: Optional[str] = None
    Production: Optional[str] = None
    Website: Optional[str] = None
    Response: Optional[str] = None
    totalSeasons: Optional[str] = None
    Season: Optional[str] = None
    Episode: Optional[str] = None
    seriesID: Optional[str] = None
    Error: Optional[str] = None


    @classmethod
    def from_dict(cls, movie_dict: dict):
        if movie_dict.get("Genre") != "N/A":
            movie_dict["Genre"] = [g for g in movie_dict.get("Genre", "").split(',')]
        else:
            movie_dict["Genre"] = []

        if movie_dict.get("Actors") != "N/A":
            movie_dict["Actors"] = [a for a in movie_dict.get("Actors", "").split(',')]
        else:
            movie_dict["Actors"] = []
        return cls(**movie_dict)

    def to_domain(self):
        data = asdict(self)
        if "Ratings" in data and data["Ratings"] is not None:
            data["Ratings"] = [
                Rating(imdbID=data.get("imdbID", ""), **r) for r in data["Ratings"]
            ]
        
        # Ustaw wartości domyślne dla brakujących pól (Movie wymaga wszystkich pól jako str)
        defaults = {
            "Title": "", "Year": "", "Rated": "N/A", "Released": "N/A",
            "Runtime": "N/A", "Genre": [], "Director": "N/A", "Writer": "N/A",
            "Actors": [], "Plot": "N/A", "Language": "N/A", "Country": "N/A",
            "Awards": "N/A", "Poster": "N/A", "Ratings": [], "Metascore": "N/A",
            "imdbRating": "N/A", "imdbVotes": "N/A", "imdbID": "", "Type": "movie",
            "DVD": "N/A", "BoxOffice": "N/A", "Production": "N/A", "Website": "N/A",
            "Response": "False", "totalSeasons": "N/A", "Season": "N/A",
            "Episode": "N/A", "seriesID": "", "Error": ""
        }
        
        # Zastąp None wartościami domyślnymi
        for key, default_value in defaults.items():
            if data.get(key) is None:
                data[key] = default_value
        
        return Movie(**data)
