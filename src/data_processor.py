import pandas as pd
import numpy as np
from datetime import datetime
import re
import requests
from typing import Tuple
import json

class NetflixDataProcessor:
    def __init__(self, file_path: str):
        """Initialize with the path to Netflix viewing history CSV."""
        try:
            # Read CSV with specific parameters to handle the semicolon issue
            self.raw_df = pd.read_csv(
                file_path, 
                sep=',',  # Use comma as separator
                encoding='utf-8',  # Specify encoding
                on_bad_lines='skip'  # Skip problematic lines
            )
            
            # Clean column names (remove any trailing semicolons)
            self.raw_df.columns = self.raw_df.columns.str.replace(';', '')
            
            # If there's a semicolon in the Date column, clean it
            if 'Date' in self.raw_df.columns:
                self.raw_df['Date'] = self.raw_df['Date'].str.replace(';', '')
            
            print(f"Successfully loaded data with {len(self.raw_df)} rows")
            print(f"Columns found: {list(self.raw_df.columns)}")
            
        except Exception as e:
            print(f"Error loading file: {str(e)}")
            print(f"File path attempted: {file_path}")
            raise
        
        self.df = None
        
        # Initialize genre mappings
        self.movie_genres = {}
        self.tv_genres = {}
        self.fetch_genre_mappings()
    
    def fetch_genre_mappings(self) -> None:
        """Fetch genre mappings from TMDB API."""
        base_url = "https://api.themoviedb.org/3"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YWM0YWQ3YjY3MzdjMmFhZTY4N2JlNzRlYzMwZDVkMyIsIm5iZiI6MTczNjQxMjA0Ny4zMjgsInN1YiI6IjY3N2Y4YjhmMTQzMWUwNTkxYWJhZjliNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.w2fLtQhRozXOaRRD0cAjts8wWZuwuO3abamviJ_KNb4"
        }
        
        # Fetch movie genres
        try:
            response = requests.get(f"{base_url}/genre/movie/list", headers=headers)
            data = response.json()
            self.movie_genres = {genre['id']: genre['name'] for genre in data.get('genres', [])}
        except Exception as e:
            print(f"Error fetching movie genres: {str(e)}")
        
        # Fetch TV genres
        try:
            response = requests.get(f"{base_url}/genre/tv/list", headers=headers)
            data = response.json()
            self.tv_genres = {genre['id']: genre['name'] for genre in data.get('genres', [])}
        except Exception as e:
            print(f"Error fetching TV genres: {str(e)}")

    def clean_basic_data(self) -> None:
        """Clean and prepare the basic Netflix viewing history data."""
        # Create a copy of raw data
        self.df = self.raw_df.copy()
        
        # Clean date column
        self.df['Date'] = self.df['Date'].str.replace(';', '')
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d.%m.%Y')
        
        # Extract series information
        self.df['Is_Series'] = self.df['Title'].str.contains(':')
        
        # Extract series name and episode info
        def extract_series_info(title: str) -> Tuple[str, str, int]:
            if ':' not in title:
                return title, None, None
            
            parts = title.split(':')
            series_name = parts[0].strip()
            
            # Try to extract season number
            season_match = re.search(r'(\d+)\.\s*Sezon', title)
            season = int(season_match.group(1)) if season_match else None
            
            # Get episode title (last part after all colons)
            episode_title = parts[-1].strip()
            
            return series_name, episode_title, season
        
        # Apply the extraction function
        series_info = self.df['Title'].apply(extract_series_info)
        self.df['Series_Name'] = series_info.apply(lambda x: x[0])
        self.df['Episode_Title'] = series_info.apply(lambda x: x[1])
        self.df['Season'] = series_info.apply(lambda x: x[2])
        
        # Add time-based features
        self.df['Year'] = self.df['Date'].dt.year
        self.df['Month'] = self.df['Date'].dt.month
        self.df['Day'] = self.df['Date'].dt.day
        self.df['Day_of_Week'] = self.df['Date'].dt.day_name()
        self.df['Is_Weekend'] = self.df['Date'].dt.weekday.isin([5, 6])

    def get_tmdb_info(self, title: str, is_series: bool) -> dict:
        """Get information from TMDB API including genres and episode counts."""
        base_url = "https://api.themoviedb.org/3"
        search_type = "tv" if is_series else "movie"
        
        # Search for the title
        search_url = f"{base_url}/search/{search_type}"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YWM0YWQ3YjY3MzdjMmFhZTY4N2JlNzRlYzMwZDVkMyIsIm5iZiI6MTczNjQxMjA0Ny4zMjgsInN1YiI6IjY3N2Y4YjhmMTQzMWUwNTkxYWJhZjliNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.w2fLtQhRozXOaRRD0cAjts8wWZuwuO3abamviJ_KNb4"
        }
        params = {
            "query": title,
            "include_adult": False,
            "language": "en-US",
            "page": 1
        }
        
        try:
            response = requests.get(search_url, headers=headers, params=params)
            data = response.json()
            
            if data.get("results"):
                result = data["results"][0]
                series_id = result.get("id")
                
                # For TV series, fetch additional details including episode count
                if is_series and series_id:
                    series_url = f"{base_url}/tv/{series_id}"
                    series_response = requests.get(series_url, headers=headers)
                    series_data = series_response.json()
                    
                    # Calculate total episodes across all seasons
                    total_episodes = sum(season.get('episode_count', 0) 
                                       for season in series_data.get('seasons', []))
                else:
                    total_episodes = None
                
                # Convert genre IDs to names
                genre_ids = result.get("genre_ids", [])
                genre_map = self.tv_genres if is_series else self.movie_genres
                genres = [genre_map.get(gid, "Unknown") for gid in genre_ids]
                
                return {
                    "id": series_id,
                    "original_name": result.get("original_name") or result.get("original_title"),
                    "overview": result.get("overview"),
                    "popularity": result.get("popularity"),
                    "vote_average": result.get("vote_average"),
                    "vote_count": result.get("vote_count"),
                    "release_date": result.get("first_air_date") or result.get("release_date"),
                    "original_language": result.get("original_language"),
                    "genres": genres,
                    "genre_ids": genre_ids,
                    "total_episodes": total_episodes
                }
        except Exception as e:
            print(f"Error fetching TMDB data for {title}: {str(e)}")
        
        return {}

    def enrich_data(self) -> None:
        """Enrich the dataset with TMDB information including genres and episode counts."""
        # Create a mapping of unique titles to avoid repeated API calls
        unique_titles = self.df[['Series_Name', 'Is_Series']].drop_duplicates()
        
        # Get TMDB information for each unique title
        tmdb_info = {}
        for _, row in unique_titles.iterrows():
            info = self.get_tmdb_info(row['Series_Name'], row['Is_Series'])
            tmdb_info[row['Series_Name']] = info
        
        # Add genre information
        self.df['Genres'] = self.df['Series_Name'].map(
            {k: ', '.join(v.get('genres', [])) for k, v in tmdb_info.items()})
        
        # Add other TMDB information as before
        self.df['Release_Year'] = self.df['Series_Name'].map(
            {k: int(v.get('release_date', '0000')[:4]) if v.get('release_date') else None 
             for k, v in tmdb_info.items()})
        self.df['Original_Language'] = self.df['Series_Name'].map(
            {k: v.get('original_language') for k, v in tmdb_info.items()})
        self.df['Popularity'] = self.df['Series_Name'].map(
            {k: v.get('popularity') for k, v in tmdb_info.items()})
        self.df['Rating'] = self.df['Series_Name'].map(
            {k: v.get('vote_average') for k, v in tmdb_info.items()})
        
        # Add total episodes information
        self.df['Total_Episodes'] = self.df['Series_Name'].map(
            {k: v.get('total_episodes') for k, v in tmdb_info.items()})

    def process_data(self) -> pd.DataFrame:
        """Run the complete data processing pipeline."""
        self.clean_basic_data()
        self.enrich_data()
        return self.df 