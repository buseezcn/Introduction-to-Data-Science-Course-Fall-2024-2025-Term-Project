from src.data_processor import NetflixDataProcessor
import pandas as pd

def main():
    # Initialize the data processor
    processor = NetflixDataProcessor('data/raw/NetflixViewingHistory_Buse.csv')
    
    # Process the data
    print("Processing Netflix viewing history data...")
    processed_df = processor.process_data()
    
    # Save the processed data
    output_path = 'data/processed/netflix_processed.csv'
    processed_df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")
    
    # Print some basic statistics
    print("\nBasic Statistics:")
    print(f"Total number of entries: {len(processed_df)}")
    print(f"Date range: {processed_df['Date'].min()} to {processed_df['Date'].max()}")
    print(f"Number of unique series/movies: {processed_df['Series_Name'].nunique()}")
    print("\nTop 5 most watched series/movies:")
    print(processed_df['Series_Name'].value_counts().head())

if __name__ == "__main__":
    main() 