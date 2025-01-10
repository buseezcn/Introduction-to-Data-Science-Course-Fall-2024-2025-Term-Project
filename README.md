# Netflix Viewing History Analysis Project
By Buse Özcan

## Project Overview
This project analyzes personal Netflix viewing history data to uncover viewing patterns, preferences, and habits. Using data science techniques and visualization tools, the project provides insights into watching behavior across different time periods, genres, and series.

## Features
- Comprehensive viewing pattern analysis (daily, weekly, monthly, yearly)
- Binge-watching detection and analysis
- Genre distribution and preferences
- Weekday vs. weekend viewing habits
- Series completion statistics
- Viewing intensity heatmaps
- Language and rating analysis

## Data Source
The dataset consists of personal Netflix viewing history from 2020 onwards, obtained directly from Netflix's viewing history export feature. The data includes:
- Show/movie titles
- Episode information
- Viewing dates
- Additional metadata from TMDB API (genres, ratings, episode counts)

## Project Structure
```
netflix_analysis/
├── data/
│   ├── raw/                    # Raw Netflix viewing history CSV
│   └── processed/              # Processed and enriched dataset
├── output/  
|    ├── plots/                      # Generated visualizations
|    │   ├── binge_patterns.png
|    │   ├── daily_patterns.png
|    │   ├── genre_distribution.png
|    │   ├── genre_wordcloud.png
|    │   ├── monthly_patterns.png
|    │   ├── top_series.png
|    │   ├── viewing_heatmap.png
|    │   └── yearly_trends.png
|    ├── analysis_report.md      # Detailed analysis findings
├── src/
│   ├── data_processor.py       # Data cleaning and processing
│   ├── analysis.py            # Analysis functions
│   ├── visualization.py       # Basic visualization tools
│   └── visualization_extended.py # Advanced visualization features
├── report.tex             # LaTeX report document
├── README.md                   # Project documentation
├── requirements.txt            # Project dependencies
├── process_data.py            # Main processing script
└── analyze_viewing_history.py  # Analysis execution script
```

## Technologies Used
- Python 3.x
- Pandas for data manipulation
- Matplotlib and Seaborn for visualization
- TMDB API for content metadata
- NumPy for numerical operations
- Wordcloud for genre visualization

## Installation
1. Clone the repository
2. Install required packages: 
```bash
pip install -r requirements.txt
```

## Usage
1. Place your Netflix viewing history CSV in `data/raw/`
2. Run the processing script: 
```bash
python process_data.py
```
3. Run the analysis script to generate visualizations and insights:
```bash
python analyze_viewing_history.py
```

This will generate:
- Viewing pattern visualizations in `plots/`
  - Daily/weekly/monthly patterns
  - Genre distribution
  - Binge-watching analysis
  - Viewing heatmaps
- Analysis report in `output/`
  - Detailed statistics
  - Content preferences
  - Viewing behavior insights

## Analysis Features
1. **Viewing Patterns**
   - Daily/weekly/monthly/yearly trends
   - Peak viewing times
   - Seasonal patterns

2. **Content Analysis**
   - Most watched series
   - Genre preferences
   - Language distribution
   - Rating analysis

3. **Behavioral Insights**
   - Binge-watching patterns
   - Series completion rates
   - Weekday vs. weekend habits

4. **Visualizations**
   - Time-based trend plots
   - Genre distribution charts
   - Viewing heatmaps
   - Word clouds
   - Series completion graphs

## Future Enhancements
- Integration with additional streaming platforms
- Mood analysis based on genre patterns
- Recommendation system development
- Social viewing pattern analysis
- Content release impact analysis

## Dependencies
- pandas
- numpy
- matplotlib
- seaborn
- requests
- jupyter
- wordcloud
- tabulate

## License
This project is for educational purposes as part of the Introduction to Data Science Course Fall 2024-2025.

## Acknowledgments
- Netflix for providing user data export functionality
- TMDB API for additional content metadata
- Introduction to Data Science Course instructors and peers

## Contact
Buse Özcan

