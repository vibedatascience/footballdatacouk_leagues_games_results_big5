import pandas as pd
import requests
from io import BytesIO
from datetime import datetime

def download_current_season():
    
    season_str = "2025/26"
    url_component = "2526"
    start_year = 2025
    
    file_extension = 'xlsx'
    url = f"https://www.football-data.co.uk/mmz4281/{url_component}/all-euro-data-{start_year}-{start_year+1}.{file_extension}"
    
    print(f"Downloading {season_str} season data...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        league_tabs = {
            'E0': 'Premier League',
            'I1': 'Serie A', 
            'SP1': 'La Liga',
            'D1': 'Bundesliga',
            'F1': 'Ligue 1'
        }
        
        all_data = []
        
        for tab, league_name in league_tabs.items():
            try:
                df = pd.read_excel(BytesIO(response.content), sheet_name=tab)
                
                df['League'] = league_name
                df['Season'] = season_str
                
                all_data.append(df)
                print(f"  ✓ {league_name}: {len(df)} matches")
            except Exception as e:
                print(f"  ✗ Error processing {league_name} ({tab}): {e}")
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            print(f"\nTotal matches downloaded: {len(combined_df)}")
            
            print("\nMatches by League:")
            print(combined_df['League'].value_counts())
            
            clean_df = clean_data(combined_df)
            
            return clean_df
        else:
            print("❌ No data extracted")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading data: {e}")
        print("\nPossible reasons:")
        print("1. The 2025-26 season file might not be available yet")
        print("2. The URL structure might have changed")
        print("3. Network connectivity issues")
        return None

def clean_data(df):
    
    print("\n📊 Cleaning data...")
    
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
    
    required_cols = ['Season', 'League', 'Date', 'HomeTeam', 'AwayTeam', 
                    'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR',
                    'HS', 'AS', 'HST', 'AST', 'HC', 'AC', 'HF', 'AF',
                    'HY', 'AY', 'HR', 'AR']
    
    existing_cols = [col for col in required_cols if col in df.columns]
    clean_df = df[existing_cols].copy()
    
    clean_df = clean_df.rename(columns=column_mapping)
    
    def convert_date(date_str):
        if pd.isna(date_str):
            return None
        
        date_str = str(date_str).strip()
        
        if ' ' in date_str:
            date_str = date_str.split(' ')[0]
        
        formats = [
            '%d/%m/%Y',
            '%d/%m/%y',
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d-%m-%Y',
        ]
        
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%Y-%m-%d')
            except:
                continue
        
        return date_str
    
    clean_df['MatchDate'] = clean_df['MatchDate'].apply(convert_date)
    
    final_columns = ['Season', 'League', 'MatchDate', 'HomeTeam', 'AwayTeam',
                    'FullTimeHomeGoals', 'FullTimeAwayGoals', 'FullTimeResult',
                    'HalfTimeHomeGoals', 'HalfTimeAwayGoals', 'HalfTimeResult',
                    'HomeShots', 'AwayShots', 'HomeShotsOnTarget', 'AwayShotsOnTarget',
                    'HomeCorners', 'AwayCorners', 'HomeFouls', 'AwayFouls',
                    'HomeYellowCards', 'AwayYellowCards', 'HomeRedCards', 'AwayRedCards']
    
    available_columns = [col for col in final_columns if col in clean_df.columns]
    clean_df = clean_df[available_columns]
    
    numeric_columns = ['FullTimeHomeGoals', 'FullTimeAwayGoals', 'HalfTimeHomeGoals', 
                      'HalfTimeAwayGoals', 'HomeShots', 'AwayShots', 
                      'HomeShotsOnTarget', 'AwayShotsOnTarget', 'HomeCorners', 
                      'AwayCorners', 'HomeFouls', 'AwayFouls', 'HomeYellowCards', 
                      'AwayYellowCards', 'HomeRedCards', 'AwayRedCards']
    
    for col in numeric_columns:
        if col in clean_df.columns:
            clean_df[col] = pd.to_numeric(clean_df[col], errors='coerce')
    
    clean_df = clean_df.sort_values(['League', 'MatchDate'])
    
    return clean_df

def append_to_historical_data(latest_df):
    
    historical_file = 'footballdatacouk_leagues_games_results_2000_2024.csv'
    
    try:
        print(f"\n📁 Reading historical data from {historical_file}...")
        historical_df = pd.read_csv(historical_file)
        print(f"  Historical data: {len(historical_df)} matches")
        
        print("\n🔄 Combining historical and latest data...")
        combined_df = pd.concat([historical_df, latest_df], ignore_index=True)
        
        combined_df = combined_df.sort_values(['Season', 'League', 'MatchDate'])
        
        output_file = 'footballdatacouk_leagues_games_results_2000_ytd.csv'
        combined_df.to_csv(output_file, index=False)
        
        print(f"✅ Combined data saved to {output_file}")
        print(f"  Total matches: {len(combined_df)}")
        
        print("\nSeason Summary:")
        season_counts = combined_df.groupby('Season').size()
        print(f"  First season: {season_counts.index[0]} ({season_counts.iloc[0]} matches)")
        print(f"  Last season: {season_counts.index[-1]} ({season_counts.iloc[-1]} matches)")
        print(f"  Total seasons: {len(season_counts)}")
        
        return combined_df
        
    except FileNotFoundError:
        print(f"⚠️ Historical file {historical_file} not found")
        print("  Saving only the latest data...")
        
        output_file = 'footballdatacouk_leagues_games_results_2000_ytd.csv'
        latest_df.to_csv(output_file, index=False)
        print(f"✅ Latest data saved to {output_file}")
        
        return latest_df

def main():
    
    print("="*60)
    print("FOOTBALL DATA UPDATER - 2025/26 Season")
    print("="*60)
    
    latest_df = download_current_season()
    
    if latest_df is not None:
        latest_file = 'footballdatacouk_leagues_games_results_2025_latest.csv'
        latest_df.to_csv(latest_file, index=False)
        print(f"\n✅ Latest season saved to {latest_file}")
        print(f"  Matches: {len(latest_df)}")
        print(f"  Date range: {latest_df['MatchDate'].min()} to {latest_df['MatchDate'].max()}")
        
        print("\nLeague Statistics for 2025/26:")
        for league in latest_df['League'].unique():
            league_data = latest_df[latest_df['League'] == league]
            total_goals = league_data['FullTimeHomeGoals'].sum() + league_data['FullTimeAwayGoals'].sum()
            matches = len(league_data)
            if matches > 0:
                print(f"  {league}: {matches} matches, {total_goals:.0f} goals ({total_goals/matches:.2f} per match)")
        
        combined_df = append_to_historical_data(latest_df)
        
        print("\n" + "="*60)
        print("PROCESS COMPLETED SUCCESSFULLY")
        print("="*60)
        print("\nFiles created:")
        print(f"  1. {latest_file} - Current season only")
        print(f"  2. footballdatacouk_leagues_games_results_2000_ytd.csv - All seasons combined")
        
    else:
        print("\n❌ Failed to download current season data")

if __name__ == "__main__":
    main()