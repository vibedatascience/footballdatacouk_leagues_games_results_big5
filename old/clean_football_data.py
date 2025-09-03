import pandas as pd
from datetime import datetime

def clean_football_data():
    """Clean and transform the football data with selected columns and proper naming"""
    
    print("Reading combined football data...")
    df = pd.read_csv('combined_football_data.csv', low_memory=False)
    
    # Column mapping
    column_mapping = {
        'Date': 'MatchDate',
        'FTHG': 'FullTimeHomeGoals',
        'FTAG': 'FullTimeAwayGoals',
        'FTR': 'FullTimeResult',
        'HTHG': 'HalfTimeHomeGoals',
        'HTAG': 'HalfTimeAwayGoals',
        'HTR': 'HalfTimeResult',
        'HS': 'HomeShots',
        'AS': 'AwayShots',
        'HST': 'HomeShotsOnTarget',
        'AST': 'AwayShotsOnTarget',
        'HC': 'HomeCorners',
        'AC': 'AwayCorners',
        'HF': 'HomeFouls',
        'AF': 'AwayFouls',
        'HY': 'HomeYellowCards',
        'AY': 'AwayYellowCards',
        'HR': 'HomeRedCards',
        'AR': 'AwayRedCards'
    }
    
    # Select required columns (original names)
    required_cols = ['Season', 'League', 'Date', 'HomeTeam', 'AwayTeam', 
                    'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR',
                    'HS', 'AS', 'HST', 'AST', 'HC', 'AC', 'HF', 'AF',
                    'HY', 'AY', 'HR', 'AR']
    
    # Check which columns exist
    existing_cols = [col for col in required_cols if col in df.columns]
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"Warning: Missing columns: {missing_cols}")
    
    # Select existing columns
    clean_df = df[existing_cols].copy()
    
    # Rename columns
    clean_df = clean_df.rename(columns=column_mapping)
    
    # Convert date format
    print("Converting date format...")
    
    def convert_date(date_str):
        """Convert date from various formats to YYYY-MM-DD"""
        if pd.isna(date_str):
            return None
        
        date_str = str(date_str).strip()
        
        # Check if it's already a datetime with timestamp (e.g., "2003-01-29 00:00:00")
        if ' ' in date_str:
            date_str = date_str.split(' ')[0]  # Take only the date part
        
        # Try different date formats
        formats = [
            '%d/%m/%Y',   # DD/MM/YYYY
            '%d/%m/%y',   # DD/MM/YY
            '%Y-%m-%d',   # Already in correct format
            '%m/%d/%Y',   # MM/DD/YYYY (just in case)
            '%d-%m-%Y',   # DD-MM-YYYY
        ]
        
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%Y-%m-%d')
            except:
                continue
        
        print(f"Could not parse date: {date_str}")
        return date_str
    
    clean_df['MatchDate'] = clean_df['MatchDate'].apply(convert_date)
    
    # Reorder columns to match requested order
    final_columns = ['Season', 'League', 'MatchDate', 'HomeTeam', 'AwayTeam',
                    'FullTimeHomeGoals', 'FullTimeAwayGoals', 'FullTimeResult',
                    'HalfTimeHomeGoals', 'HalfTimeAwayGoals', 'HalfTimeResult',
                    'HomeShots', 'AwayShots', 'HomeShotsOnTarget', 'AwayShotsOnTarget',
                    'HomeCorners', 'AwayCorners', 'HomeFouls', 'AwayFouls',
                    'HomeYellowCards', 'AwayYellowCards', 'HomeRedCards', 'AwayRedCards']
    
    # Ensure all columns are in the correct order
    clean_df = clean_df[final_columns]
    
    # Convert numeric columns to appropriate types
    numeric_columns = ['FullTimeHomeGoals', 'FullTimeAwayGoals', 'HalfTimeHomeGoals', 
                      'HalfTimeAwayGoals', 'HomeShots', 'AwayShots', 
                      'HomeShotsOnTarget', 'AwayShotsOnTarget', 'HomeCorners', 
                      'AwayCorners', 'HomeFouls', 'AwayFouls', 'HomeYellowCards', 
                      'AwayYellowCards', 'HomeRedCards', 'AwayRedCards']
    
    for col in numeric_columns:
        if col in clean_df.columns:
            clean_df[col] = pd.to_numeric(clean_df[col], errors='coerce')
    
    # Sort by Season and MatchDate
    clean_df = clean_df.sort_values(['Season', 'League', 'MatchDate'])
    
    # Save to CSV
    output_file = 'clean_football_data.csv'
    clean_df.to_csv(output_file, index=False)
    
    print(f"\n✅ Clean data saved to {output_file}")
    print(f"Total rows: {len(clean_df)}")
    print(f"Columns: {list(clean_df.columns)}")
    
    # Print summary statistics
    print("\n📊 Data Summary:")
    print(f"Seasons: {clean_df['Season'].nunique()}")
    print(f"Leagues: {clean_df['League'].nunique()}")
    print(f"Date range: {clean_df['MatchDate'].min()} to {clean_df['MatchDate'].max()}")
    
    print("\nMatches per League:")
    print(clean_df['League'].value_counts())
    
    print("\nSample of cleaned data:")
    print(clean_df.head())
    
    return clean_df

if __name__ == "__main__":
    clean_football_data()