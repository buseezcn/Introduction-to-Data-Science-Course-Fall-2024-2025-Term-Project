import pandas as pd
import matplotlib.pyplot as plt
from src.analysis import NetflixAnalyzer
from src.visualization_extended import NetflixExtendedVisualizer
from datetime import datetime
import os
from tabulate import tabulate

def create_analysis_report(analyzer, patterns, binge_sessions, output_dir):
    """Create a detailed markdown report with analysis results."""
    
    # Calculate additional statistics
    total_watch_time = len(patterns['most_watched_series']) * 30  # Approximate minutes per episode
    avg_episodes_per_day = len(patterns['most_watched_series']) / len(patterns['most_watched_series'].index.unique())
    peak_month = analyzer.df.groupby(analyzer.df['Date'].dt.strftime('%B'))['Title'].count().idxmax()
    peak_year = analyzer.df.groupby('Year').size().idxmax()
    
    # Create the report content
    report = [
        "# Netflix Viewing History Analysis Report",
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        
        "## Executive Summary",
        "This report provides a comprehensive analysis of my Netflix viewing habits, including patterns, preferences, and binge-watching behavior.\n",
        
        "## Overall Statistics",
        f"- Total Views: {patterns['total_views']}",
        f"- Unique Series/Movies Watched: {patterns['unique_series']}",
        f"- Estimated Total Watch Time: {total_watch_time//60:,} hours ({total_watch_time//1440:,} days)",
        f"- Average Episodes per Day: {avg_episodes_per_day:.2f}",
        f"- Peak Viewing Month: {peak_month}",
        f"- Peak Viewing Year: {peak_year}",
        f"- Most Active Viewing Day: {patterns['favorite_day']}",
        f"- Weekend Viewing Ratio: {patterns['weekend_ratio']:.2%}\n",
        
        "## Content Preferences",
        "### Top 10 Most Watched Series",
        tabulate(
            patterns['most_watched_series'].head(10).reset_index(),
            headers=['Series', 'Episodes Watched'],
            tablefmt='pipe'
        ),
        
        "\n### Series Completion Analysis",
        "Series completion percentage based on total available episodes:",
        tabulate(
            analyzer.get_series_completion_stats().head(10),
            headers=['Series', 'Episodes Watched', 'Total Episodes', 'Completion %'],
            tablefmt='pipe'
        ),
        
        "\n## Binge-Watching Analysis",
        f"Total Binge-Watching Sessions: {len(binge_sessions)}",
        f"Average Episodes per Binge: {binge_sessions['Episodes_Watched'].mean():.2f}",
        
        "\n### Top 10 Most Binge-Watched Series",
        tabulate(
            binge_sessions.groupby('Series_Name')['Episodes_Watched'].count().sort_values(ascending=False).head(10).reset_index(),
            headers=['Series', 'Binge Sessions'],
            tablefmt='pipe'
        ),
        
        "\n### Most Intense Binge Sessions",
        tabulate(
            binge_sessions.nlargest(10, 'Episodes_Watched')[
                ['Series_Name', 'Episodes_Watched', 'Date', 'Episode_Title']
            ],
            headers=['Series', 'Episodes', 'Date', 'Episodes List'],
            tablefmt='pipe'
        ),
        
        "\n## Content Analysis",
        "### Genre Distribution",
        tabulate(
            analyzer.get_genre_statistics().head(10),
            headers=['Genre', 'Count', 'Percentage'],
            tablefmt='pipe'
        ),
        
        "\n### Language Diversity",
        tabulate(
            analyzer.get_language_statistics().head(10),
            headers=['Language', 'Count', 'Percentage'],
            tablefmt='pipe'
        ),
        
        "\n### Temporal Viewing Patterns",
        "#### Daily Distribution",
        tabulate(
            analyzer.get_daily_viewing_statistics(),
            headers=['Day', 'Views', 'Percentage'],
            tablefmt='pipe'
        ),
        
        "\n#### Monthly Trends",
        tabulate(
            analyzer.get_monthly_viewing_statistics(),
            headers=['Month', 'Views', 'Percentage'],
            tablefmt='pipe'
        ),
        
        "\n## Rating Analysis",
        "### Top Rated Content Watched",
        tabulate(
            analyzer.get_top_rated_content().head(10),
            headers=['Title', 'Rating', 'Genre'],
            tablefmt='pipe'
        ),
        
        "\n### Average Ratings by Genre",
        tabulate(
            analyzer.get_genre_ratings(),
            headers=['Genre', 'Average Rating', 'Count'],
            tablefmt='pipe'
        ),
        
        "\n## Viewing Behavior Insights",
        "- " + "\n- ".join([
            f"I tend to watch more content on {analyzer.df['Day_of_Week'].mode().iloc[0]}s",
            "My binge-watching sessions are most common during weekends" if analyzer.df['Is_Weekend'].mean() > 0.3 else "I prefer spreading my viewing throughout the week",
            f"My most watched genre is {analyzer.get_genre_statistics().iloc[0]['Genre']}",
            f"I watch content in {len(analyzer.df['Original_Language'].unique())} different languages",
            f"The average rating of content I watch is {analyzer.df['Rating'].mean():.1f}/10"
        ]),
    ]
    
    # Write the report
    with open(os.path.join(output_dir, 'analysis_report.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

def analyze_netflix_history():
    # Create output directories
    output_dir = 'output'
    plots_dir = os.path.join(output_dir, 'plots')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(plots_dir, exist_ok=True)
    
    # Load the processed data
    df = pd.read_csv('data/processed/netflix_processed.csv')
    df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date is datetime
    
    # Initialize analyzers
    analyzer = NetflixAnalyzer(df)
    visualizer = NetflixExtendedVisualizer(df)
    
    # 1. Analyze viewing patterns
    patterns = analyzer.analyze_viewing_patterns()
    binge_sessions = analyzer.detect_binge_watching(threshold_hours=24)
    
    # 2. Generate and save visualizations
    print("\n=== Generating Visualizations ===")
    visualizations = {
        'monthly_patterns': visualizer.plot_monthly_viewing_patterns,
        'genre_distribution': visualizer.plot_genre_distribution,
        'viewing_heatmap': visualizer.plot_viewing_heatmap,
        'genre_wordcloud': visualizer.create_genre_wordcloud,
        'daily_patterns': visualizer.plot_viewing_by_day,
        'yearly_trends': visualizer.plot_yearly_trends,
        'top_series': visualizer.plot_top_series,
        'binge_patterns': visualizer.plot_binge_watching_patterns
    }
    
    for name, plot_func in visualizations.items():
        plt.figure(figsize=(12, 6))
        plot_func()
        plt.savefig(os.path.join(plots_dir, f'{name}.png'), bbox_inches='tight', dpi=300)
        plt.close()
    
    # 3. Generate analysis report
    print("\n=== Generating Analysis Report ===")
    create_analysis_report(analyzer, patterns, binge_sessions, output_dir)

if __name__ == "__main__":
    print("Starting Netflix viewing history analysis...")
    analyze_netflix_history()
    print("\nAnalysis complete. Results saved in 'output' directory.") 