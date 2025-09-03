import pandas as pd
import requests
import os
import sys
from io import BytesIO

def generate_seasons():
    """Generate season strings and URL components from 2000/01 to 2024/25"""
    seasons = []
    for start_year in range(2000, 2025):
        end_year = start_year + 1
        season_str = f"{start_year}/{str(end_year)[-2:]}"
        url_component = f"{str(start_year)[-2:]}{str(end_year)[-2:]}"
        seasons.append((season_str, url_component, start_year))
    return seasons

def download_and_process_season(season_str, url_component, start_year):
    """Download and process data for a single season"""
    
    file_extension = 'xls' if start_year <= 2002 else 'xlsx'
    url = f"https://www.football-data.co.uk/mmz4281/{url_component}/all-euro-data-{start_year}-{start_year+1}.{file_extension}"
    
    print(f"Downloading {season_str} from {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        league_tabs = {
            'E0': 'Premier League',
            'I1': 'Serie A', 
            'SP1': 'La Liga',
            'D1': 'Bundesliga',  # D1 is German Bundesliga
            'F1': 'Ligue 1'
        }
        
        all_data = []
        
        for tab, league_name in league_tabs.items():
            try:
                df = pd.read_excel(BytesIO(response.content), sheet_name=tab)
                
                df['League'] = league_name
                df['Season'] = season_str
                
                all_data.append(df)
                print(f"  - Processed {league_name}: {len(df)} rows")
            except Exception as e:
                print(f"  - Error processing {league_name} ({tab}): {e}")
        
        if all_data:
            season_df = pd.concat(all_data, ignore_index=True)
            print(f"  Total rows for {season_str}: {len(season_df)}")
            return season_df
        else:
            print(f"  No data extracted for {season_str}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"  Error downloading {season_str}: {e}")
        return None

def main():
    """Main function to download and combine all football data"""
    
    print("Starting football data download...")
    sys.stdout.flush()
    
    seasons = generate_seasons()
    all_seasons_data = []
    
    for season_str, url_component, start_year in seasons:
        season_data = download_and_process_season(season_str, url_component, start_year)
        if season_data is not None:
            all_seasons_data.append(season_data)
    
    if all_seasons_data:
        combined_df = pd.concat(all_seasons_data, ignore_index=True)
        
        output_file = 'combined_football_data.csv'
        combined_df.to_csv(output_file, index=False)
        print(f"\n✅ Combined data saved to {output_file}")
        print(f"Total rows: {len(combined_df)}")
        print(f"Total seasons processed: {len(all_seasons_data)}")
        
        print("\nSummary by League:")
        league_summary = combined_df.groupby('League').size()
        print(league_summary)
        
        print("\nSummary by Season:")
        season_summary = combined_df.groupby('Season').size()
        print(season_summary)
    else:
        print("❌ No data was successfully downloaded")

if __name__ == "__main__":
    main()