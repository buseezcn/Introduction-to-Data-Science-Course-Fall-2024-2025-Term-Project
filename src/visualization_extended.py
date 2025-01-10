from typing import Optional, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
from wordcloud import WordCloud
import numpy as np

class NetflixExtendedVisualizer:
    def __init__(self, df: pd.DataFrame):
        """Initialize with processed Netflix data."""
        self.df = df
        # Use a basic style instead of seaborn
        plt.style.use('default')
        # Set consistent colors and style
        self.colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#99CCFF', '#FFB366', '#FF99FF']
        plt.rcParams['figure.figsize'] = [12, 6]
        
        # Convert Date column to datetime if it's not already
        if 'Date' in self.df.columns and not pd.api.types.is_datetime64_any_dtype(self.df['Date']):
            self.df['Date'] = pd.to_datetime(self.df['Date'])
    
    def generate_all_visualizations(self, save_path: Optional[str] = None) -> None:
        """Generate all visualizations and optionally save them."""
        self.plot_monthly_viewing_patterns()
        self.plot_genre_distribution()
        self.plot_viewing_heatmap()
        self.plot_binge_watching_patterns()
        self.plot_top_series()
        self.create_genre_wordcloud()
        self.plot_viewing_by_day()
        self.plot_yearly_trends()
        
    def plot_monthly_viewing_patterns(self) -> None:
        """Plot monthly viewing patterns."""
        monthly_views = self.df.groupby(pd.Grouper(key='Date', freq='ME'))['Title'].count()
        
        plt.plot(monthly_views.index, monthly_views.values)
        plt.title('Monthly Viewing Patterns')
        plt.xlabel('Month')
        plt.ylabel('Number of Views')
        plt.xticks(rotation=45)
        plt.grid(True)
        # Don't call plt.show() here

    def plot_genre_distribution(self) -> None:
        """Create a pie chart of genre distribution."""
        # Split multiple genres and count each occurrence
        genres = [genre.strip() for genres in self.df['Genres'].dropna() 
                 for genre in genres.split(',')]
        genre_counts = pd.Series(genres).value_counts()
        
        plt.figure(figsize=(12, 8))
        plt.pie(genre_counts.values[:8], labels=genre_counts.index[:8], 
                autopct='%1.1f%%', colors=self.colors)
        plt.title('Top 8 Genre Distribution')
        plt.axis('equal')
        # Remove plt.show()

    def plot_viewing_heatmap(self) -> None:
        """Create a heatmap of viewing patterns by day and month."""
        viewing_matrix = pd.crosstab(self.df['Date'].dt.month, 
                                   self.df['Date'].dt.day_name())
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(viewing_matrix, cmap='YlOrRd', annot=True, fmt='d')
        plt.title('Viewing Heatmap (Month vs Day)')
        plt.xlabel('Day of Week')
        plt.ylabel('Month')
        plt.tight_layout()
        # Remove plt.show()

    def create_genre_wordcloud(self) -> None:
        """Create a word cloud visualization of genres."""
        genres_text = ' '.join([genres for genres in self.df['Genres'].dropna()])
        wordcloud = WordCloud(width=800, height=400, 
                            background_color='white',
                            colormap='viridis').generate(genres_text)
        
        plt.figure(figsize=(15, 7))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Genre Word Cloud')
        # Remove plt.show()

    def plot_viewing_by_day(self) -> None:
        """Plot viewing activity by day of week."""
        daily_counts = self.df['Day_of_Week'].value_counts()
        # Reorder days
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                     'Friday', 'Saturday', 'Sunday']
        daily_counts = daily_counts.reindex(days_order)
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(daily_counts.index, daily_counts.values, 
                      color=self.colors[:7])
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        plt.title('Viewing Activity by Day of Week')
        plt.xlabel('Day of Week')
        plt.ylabel('Number of Views')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        # Remove plt.show()

    def plot_yearly_trends(self) -> None:
        """Plot yearly viewing trends with genre breakdown."""
        yearly_views = self.df.groupby('Year').size()
        
        plt.figure(figsize=(12, 6))
        plt.plot(yearly_views.index, yearly_views.values, 
                marker='o', color=self.colors[0], linewidth=2)
        plt.title('Yearly Viewing Trends')
        plt.xlabel('Year')
        plt.ylabel('Number of Views')
        plt.grid(True, alpha=0.3)
        
        # Add value labels
        for x, y in zip(yearly_views.index, yearly_views.values):
            plt.text(x, y, f'{int(y)}', ha='center', va='bottom')
        
        plt.tight_layout()
        # Remove plt.show()

    def plot_top_series(self, top_n: int = 10) -> None:
        """Plot top N most watched series."""
        series_counts = self.df['Series_Name'].value_counts().head(top_n)
        
        plt.figure(figsize=(15, 8))
        bars = plt.barh(series_counts.index, series_counts.values, 
                       color=self.colors[:top_n])
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2.,
                    f'{int(width)}',
                    ha='left', va='center')
        
        plt.title(f'Top {top_n} Most Watched Series')
        plt.xlabel('Number of Episodes Watched')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        # Remove plt.show()

    def plot_binge_watching_patterns(self, min_episodes: int = 3) -> None:
        """Plot binge-watching patterns (days with multiple episodes)."""
        daily_counts = self.df.groupby(['Date', 'Series_Name']).size()
        binge_days = daily_counts[daily_counts >= min_episodes]
        
        if not binge_days.empty:
            plt.figure(figsize=(15, 7))
            plt.hist(binge_days.values, bins=20, color=self.colors[0], 
                    alpha=0.7, edgecolor='black')
            plt.title('Distribution of Binge-Watching Sessions')
            plt.xlabel('Number of Episodes per Day')
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            # Remove plt.show() 