from dataclasses import dataclass
from typing import List


@dataclass
class Rating:
    imdbID: str
    Source: str
    Value: str

@dataclass
class Movie:
    Title: str
    Year: str
    Rated: str
    Released: str
    Runtime: str
    Genre: List[str]
    Director: str
    Writer: str
    Actors: List[str]
    Plot: str
    Language: str
    Country: str
    Awards: str
    Poster: str
    Ratings: List[Rating]
    Metascore: str
    imdbRating: str
    imdbVotes: str
    imdbID: str
    Type: str
    DVD: str
    BoxOffice: str
    Production: str
    Website: str
    Response: str
    Error:str
    TotalSeasons: str
