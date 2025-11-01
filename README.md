# Advanced Data Mining - Movie Data Collector

A Python application for collecting and storing movie data from the OMDB (Open Movie Database) API. This project demonstrates advanced data mining techniques, clean architecture principles, and PEP 8 compliant code.

## Features

- **Automated Movie Data Collection**: Fetches movie data from OMDB API incrementally by IMDB ID
- **SQLite Database Storage**: Stores movie information, ratings, genres, and actors in a relational database
- **Resume Capability**: Automatically resumes from the last processed movie ID
- **Error Handling**: Implements retry logic with exponential backoff for API failures
- **Logging**: Comprehensive logging to both file and console
- **Clean Architecture**: Follows SOLID principles with interfaces, dependency injection, and separation of concerns
- **Type Hints**: Full type annotations for better code maintainability
- **Unit Tests**: Comprehensive test suite for all components

## Project Structure

```
AdvancedDataMining/
├── config/
│   ├── appsettings.json       # Application configuration
│   └── AppSettings.py         # Settings loader
├── src/
│   ├── interfaces/            # Abstract interfaces
│   │   ├── i_movie_data_writer.py
│   │   ├── i_movie_logger.py
│   │   └── i_omdb_client.py
│   ├── models/
│   │   ├── domain/            # Domain models
│   │   │   └── movie_data.py
│   │   └── dto/               # Data Transfer Objects
│   │       └── movie_data_dto.py
│   └── services/              # Business logic implementations
│       ├── get_data_wrapper.py
│       ├── movie_data_writer.py
│       ├── movie_logger.py
│       └── omdb_client.py
├── tests/                     # Unit tests
│   ├── GetDataWrapperTests.py
│   ├── MovieDataWriterTests.py
│   ├── MovieLoggerTests.py
│   └── OmdbClientTests.py
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
└── README.md

```

## Requirements

- Python 3.7+
- OMDB API key (free at http://www.omdbapi.com/apikey.aspx)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AdvancedDataMining
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your OMDB API key:
   - Get your free API key from http://www.omdbapi.com/apikey.aspx
   - Edit `config/appsettings.json` and replace the `apiKey` value:
```json
{
  "apiKey": "your_api_key_here",
  "startFromId": null,
  "stopAtId": null
}
```

## Configuration

The `config/appsettings.json` file supports the following settings:

- **apiKey** (required): Your OMDB API key
- **startFromId** (optional): Starting IMDB ID (e.g., "tt0000001"). If null, starts from the last processed ID or "tt0000000"
- **stopAtId** (optional): Stopping IMDB ID (e.g., "tt0001000"). If null, runs indefinitely until manually stopped

## Usage

Run the application:

```bash
python main.py
```

The application will:
1. Connect to the OMDB API using your configured API key
2. Start fetching movies from the last processed ID (or from "tt0000000" if starting fresh)
3. Save movie data to `movies.db` SQLite database
4. Log all operations to `movies.log` and console
5. Continue until manually stopped or until `stopAtId` is reached

### Database Schema

The application creates the following tables:

- **movies**: Stores movie information (title, year, director, plot, ratings, etc.)
- **ratings**: Stores individual ratings from different sources (IMDB, Rotten Tomatoes, Metacritic)
- **genres**: Stores unique genres
- **actors**: Stores unique actors

## Architecture

The project follows clean architecture principles:

- **Interfaces** (`src/interfaces/`): Abstract base classes defining contracts
- **Domain Models** (`src/models/domain/`): Core business entities
- **DTOs** (`src/models/dto/`): Data transfer objects for API responses
- **Services** (`src/services/`): Business logic implementations
- **Dependency Injection**: Services are injected via constructors, enabling easy testing and mocking

## Key Components

### GetDataWrapper
Orchestrates the data collection process:
- Manages the fetching loop
- Handles IMDB ID incrementing
- Coordinates between API client, data writer, and logger

### OmdbClient
HTTP client for OMDB API:
- Fetches movie data by IMDB ID
- Returns responses as `requests.Response` objects

### MovieDataWriter
Database persistence layer:
- Implements context manager for automatic connection handling
- Saves movies, ratings, genres, and actors
- Commits in batches (every 1000 movies)
- Tracks the latest processed movie ID

### MovieLogger
Logging service:
- Logs to both file (`movies.log`) and console
- Provides info and error logging methods

## Testing

Run the test suite:

```bash
python -m unittest discover -s tests
```

Or run individual test files:

```bash
python -m unittest tests.GetDataWrapperTests
python -m unittest tests.MovieDataWriterTests
python -m unittest tests.MovieLoggerTests
python -m unittest tests.OmdbClientTests
```

## Code Style

This project strictly adheres to **PEP 8** Python style guidelines:
- All module names use `snake_case`
- All class names use `PascalCase`
- All function and variable names use `snake_case`
- Type hints are used throughout

## Error Handling

- **API Failures**: Implements retry logic (up to 3 attempts) with exponential backoff
- **Connection Errors**: Raises `ConnectionError` after max retries
- **Invalid Movie IDs**: Logs errors but continues processing
- **Database Errors**: Handled by context manager, ensures proper cleanup

## IMDB ID Format

IMDB IDs follow the format: `tt` followed by 7 digits (e.g., `tt0000001`, `tt1234567`).

The application automatically increments IDs and handles the padding correctly.

## Logging

Logs are written to:
- **File**: `movies.log` (in project root)
- **Console**: Standard output

Log format: `YYYY-MM-DD HH:MM:SS - <message>`

## Limitations

- Free OMDB API has rate limits (1000 requests per day)
- Database operations commit every 1000 movies (not after each movie)
- Requires internet connection to fetch data from OMDB API

## Future Enhancements

- Support for parallel processing
- Configurable batch commit size
- Progress bar display
- Database migration tools
- Support for multiple data sources
- Data export functionality

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Advanced Data Mining Course

## Acknowledgments

- OMDB API (http://www.omdbapi.com/) for providing movie data
- Python community for excellent libraries and best practices

