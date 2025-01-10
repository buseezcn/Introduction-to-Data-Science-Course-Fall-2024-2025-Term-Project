import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional

class NetflixVisualizer:
    def __init__(self, df: pd.DataFrame):
        """Initialize with processed Netflix data."""
        self.df = df
        # Set style for all plots
        plt.style.use('seaborn')
        
    def plot_viewing_trends(self, frequency: str = 'daily') -> None:
        """
        Plot viewing trends over time.
        
        Args:
            frequency (str): 'daily', 'weekly', 'monthly', or 'yearly'
        """
        plt.figure(figsize=(15, 6))
        
        if frequency == 'daily':
            data = self.df['Date'].value_counts().sort_index()
            plt.title('Daily Viewing Activity')
        elif frequency == 'weekly':
            data = self.df.groupby(self.df['Date'].dt.isocalendar().week)['Title'].count()
            plt.title('Weekly Viewing Activity')
        elif frequency == 'monthly':
            data = self.df.groupby([self.df['Date'].dt.year, self.df['Date'].dt.month])['Title'].count()
            plt.title('Monthly Viewing Activity')
        else:  # yearly
            data = self.df.groupby(self.df['Date'].dt.year)['Title'].count()
            plt.title('Yearly Viewing Activity')
            
        data.plot(kind='line')
        plt.xlabel('Time')
        plt.ylabel('Number of Views')
        plt.tight_layout()
        plt.show()
        
    def create_viewing_heatmap(self) -> None:
        """Create a heatmap of viewing activity by day and hour."""
        plt.figure(figsize=(12, 8))
        viewing_matrix = pd.crosstab(self.df['Day_of_Week'], self.df['Month'])
        sns.heatmap(viewing_matrix, cmap='YlOrRd', annot=True, fmt='d')
        plt.title('Viewing Activity Heatmap')
        plt.tight_layout()
        plt.show()
        
    def plot_weekday_weekend_comparison(self) -> None:
        """Create a comparison of weekday vs weekend viewing."""
        plt.figure(figsize=(10, 6))
        self.df.groupby('Is_Weekend')['Title'].count().plot(
            kind='bar',
            title='Weekday vs Weekend Viewing'
        )
        plt.xticks([0, 1], ['Weekday', 'Weekend'])
        plt.xlabel('Day Type')
        plt.ylabel('Number of Views')
        plt.tight_layout()
        plt.show() 