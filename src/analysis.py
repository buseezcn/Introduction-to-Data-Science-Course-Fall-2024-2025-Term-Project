import pandas as pd
from datetime import timedelta
from typing import List, Dict, Any
import calendar

class NetflixAnalyzer:
    def __init__(self, df: pd.DataFrame):
        """Initialize with processed Netflix data."""
        self.df = df
        
    def detect_binge_watching(self, threshold_hours: int = 24) -> pd.DataFrame:
        """
        Detect binge-watching sessions based on number of episodes watched within threshold hours.
        
        Args:
            threshold_hours (int): Time window to consider for binge-watching (default 24 hours)
            
        Returns:
            DataFrame with binge-watching sessions
        """
        # Group by date and series, count episodes
        binge_sessions = (self.df.groupby(['Date', 'Series_Name'])
                         .agg({
                             'Title': 'count',
                             'Episode_Title': list,
                         })
                         .rename(columns={'Title': 'Episodes_Watched'})
                         )
        
        # Filter for sessions with multiple episodes
        binge_sessions = binge_sessions[binge_sessions['Episodes_Watched'] > 1]
        
        # Reset index to make Date and Series_Name regular columns
        binge_sessions = binge_sessions.reset_index()
        
        # Sort by date and number of episodes
        binge_sessions = binge_sessions.sort_values(['Date', 'Episodes_Watched'], 
                                                  ascending=[False, False])
        
        return binge_sessions
    
    def analyze_viewing_patterns(self) -> Dict[str, Any]:
        """Analyze various viewing patterns and return statistics."""
        return {
            'total_views': len(self.df),
            'unique_series': self.df['Series_Name'].nunique(),
            'most_watched_series': self.df['Series_Name'].value_counts().head(),
            'favorite_day': self.df['Day_of_Week'].value_counts().index[0],
            'weekend_ratio': self.df['Is_Weekend'].mean(),
            'viewing_by_month': self.df.groupby('Month')['Title'].count()
        } 
    
    def get_genre_statistics(self) -> pd.DataFrame:
        """Calculate genre statistics."""
        genres = [genre.strip() for genres in self.df['Genres'].dropna() 
                 for genre in genres.split(',')]
        genre_counts = pd.Series(genres).value_counts()
        total = len(genres)
        
        return pd.DataFrame({
            'Count': genre_counts,
            'Percentage': (genre_counts / total * 100).round(2).astype(str) + '%'
        }).reset_index().rename(columns={'index': 'Genre'})
    
    def get_language_statistics(self) -> pd.DataFrame:
        """Calculate language distribution statistics."""
        lang_counts = self.df['Original_Language'].value_counts()
        total = len(self.df)
        
        return pd.DataFrame({
            'Count': lang_counts,
            'Percentage': (lang_counts / total * 100).round(2).astype(str) + '%'
        }).reset_index().rename(columns={'index': 'Language'})
    
    def get_daily_viewing_statistics(self) -> pd.DataFrame:
        """Calculate daily viewing statistics."""
        daily_counts = self.df['Day_of_Week'].value_counts()
        total = len(self.df)
        
        # Reorder days
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                     'Friday', 'Saturday', 'Sunday']
        daily_counts = daily_counts.reindex(days_order)
        
        return pd.DataFrame({
            'Views': daily_counts,
            'Percentage': (daily_counts / total * 100).round(2).astype(str) + '%'
        }).reset_index().rename(columns={'index': 'Day'}) 
    
    def get_series_completion_stats(self) -> pd.DataFrame:
        """Calculate series completion statistics."""
        series_counts = self.df.groupby('Series_Name').agg({
            'Title': 'count',
            'Total_Episodes': 'first'  # Get the total episodes from TMDB data
        }).reset_index()
        
        series_counts.columns = ['Series', 'Episodes_Watched', 'Total_Episodes']
        series_counts['Completion %'] = (series_counts['Episodes_Watched'] / 
                                       series_counts['Total_Episodes'] * 100)
        
        # Handle cases where Total_Episodes might be NaN
        series_counts['Completion %'] = series_counts['Completion %'].apply(
            lambda x: f"{x:.1f}%" if pd.notnull(x) else "Unknown"
        )
        
        return series_counts.sort_values('Episodes_Watched', ascending=False)
    
    def get_monthly_viewing_statistics(self) -> pd.DataFrame:
        """Calculate monthly viewing statistics."""
        monthly_counts = self.df['Month'].value_counts()
        total = len(self.df)
        
        # Convert month numbers to names
        month_names = {i: calendar.month_name[i] for i in range(1, 13)}
        monthly_counts.index = monthly_counts.index.map(month_names)
        
        return pd.DataFrame({
            'Views': monthly_counts,
            'Percentage': (monthly_counts / total * 100).round(2).astype(str) + '%'
        }).reset_index().rename(columns={'index': 'Month'})
    
    def get_top_rated_content(self) -> pd.DataFrame:
        """Get top rated content watched."""
        return self.df.sort_values('Rating', ascending=False)[
            ['Series_Name', 'Rating', 'Genres']
        ].drop_duplicates()
    
    def get_genre_ratings(self) -> pd.DataFrame:
        """Calculate average ratings by genre."""
        genres = []
        ratings = []
        counts = []
        
        for genre in self.df['Genres'].str.split(',').explode().unique():
            if pd.isna(genre):
                continue
            genre = genre.strip()
            genre_mask = self.df['Genres'].str.contains(genre, na=False)
            avg_rating = self.df[genre_mask]['Rating'].mean()
            count = genre_mask.sum()
            
            genres.append(genre)
            ratings.append(round(avg_rating, 2))
            counts.append(count)
        
        return pd.DataFrame({
            'Genre': genres,
            'Average Rating': ratings,
            'Count': counts
        }).sort_values('Average Rating', ascending=False) 