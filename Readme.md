# Football-Data.co.uk Match Results Dataset

## Overview
Comprehensive football match results and statistics from Europe's top 5 leagues, sourced from Football-Data.co.uk. Contains detailed match-level data including goals, cards, shots, corners, and match outcomes spanning 25+ years.

## Files

| File | Coverage | Description |
|------|----------|-------------|
| `footballdatacouk_leagues_games_results_2000_2024.csv` | 2000/01 - 2024/25 | Historical data for 25 complete seasons |
| `footballdatacouk_leagues_games_results_2025_latest.csv` | 2025/26 only | Current season in progress (updated regularly) |
| `footballdatacouk_leagues_games_results_2000_ytd.csv` | 2000/01 - current | Complete dataset including latest matches |

## Quick Start

### Load Data Using Python
```python
import pandas as pd

# For historical analysis (complete seasons only)
historical = pd.read_csv('https://raw.githubusercontent.com/vibedatascience/footballdatacouk_leagues_games_results_big5/refs/heads/main/footballdatacouk_leagues_games_results_2000_2024.csv')

# For current season tracking
current = pd.read_csv('https://raw.githubusercontent.com/vibedatascience/footballdatacouk_leagues_games_results_big5/refs/heads/main/footballdatacouk_leagues_games_results_2025_latest.csv')

# For complete dataset
full = pd.read_csv('https://raw.githubusercontent.com/vibedatascience/footballdatacouk_leagues_games_results_big5/refs/heads/main/footballdatacouk_leagues_games_results_2000_ytd.csv')
```

### Download Latest Data
```python
# Run the update script to get latest 2025/26 matches
python update_football_data.py
```

## Coverage Details

### Leagues
- **Premier League** - English Premier League
- **Serie A** - Italian Serie A  
- **La Liga** - Spanish La Liga
- **Bundesliga** - German Bundesliga
- **Ligue 1** - French Ligue 1

### Seasons
- **Historical**: 2000/01 through 2024/25 (25 complete seasons)
- **Current**: 2025/26 (in progress)
- **Records**: ~95,000+ matches
- **Teams**: ~200+ unique clubs

## Data Dictionary

### Core Columns

| Column | Type | Description |
|--------|------|-------------|
| `Season` | str | Season identifier (e.g., "2024/25") |
| `League` | str | League name (e.g., "Premier League", "Serie A", "La Liga", "Bundesliga", "Ligue 1") |
| `MatchDate` | str | Match date in YYYY-MM-DD format |
| `HomeTeam` | str | Home team name |
| `AwayTeam` | str | Away team name |

### Match Results

| Column | Type | Description |
|--------|------|-------------|
| `FullTimeHomeGoals` | int | Goals scored by home team |
| `FullTimeAwayGoals` | int | Goals scored by away team |
| `FullTimeResult` | str | Match result (H=Home win, D=Draw, A=Away win) |
| `HalfTimeHomeGoals` | int | Home team goals at half-time |
| `HalfTimeAwayGoals` | int | Away team goals at half-time |
| `HalfTimeResult` | str | Half-time result (H/D/A) |

### Match Statistics

| Column | Type | Description |
|--------|------|-------------|
| `HomeShots` | int | Total shots by home team |
| `AwayShots` | int | Total shots by away team |
| `HomeShotsOnTarget` | int | Shots on target by home team |
| `AwayShotsOnTarget` | int | Shots on target by away team |
| `HomeCorners` | int | Corner kicks for home team |
| `AwayCorners` | int | Corner kicks for away team |

### Disciplinary Records

| Column | Type | Description |
|--------|------|-------------|
| `HomeFouls` | int | Fouls committed by home team |
| `AwayFouls` | int | Fouls committed by away team |
| `HomeYellowCards` | int | Yellow cards for home team |
| `AwayYellowCards` | int | Yellow cards for away team |
| `HomeRedCards` | int | Red cards for home team |
| `AwayRedCards` | int | Red cards for away team |

## Critical Usage Guidelines

### Always check the club names by getting the data first. Don't assume club names


### Promoted/Relegated Teams
Teams move between leagues due to promotion/relegation. A team may have records in different leagues across seasons.

```python
# Example: Track team's league history
team_history = df[df['HomeTeam'] == 'Leicester'].groupby(['Season', 'League']).size()
```

### Missing Data Handling
Some statistics (shots, corners, cards) may be missing for older seasons (if using this data):

```python
# Check data completeness by season
completeness = df.groupby('Season')[['HomeShots', 'HomeCorners']].count()
```

## Data Quality Notes

- **Early Seasons** (2000-2005): May have limited statistics beyond basic match results
- **Current Season**: 2025/26 data updates regularly but is incomplete
- **League Sizes**: 
  - Premier League, Serie A, La Liga, Ligue 1: 20 teams
  - Bundesliga: 18 teams
- **Date Format**: Standardized to YYYY-MM-DD across all seasons
- **Team Names**: May require standardization for consistent analysis

## Common Analysis Examples

### Calculate League Table/Standings
```python
def calculate_league_standings(df, season=None, league=None):
    """Calculate league standings based on match results"""
    season_df = df.copy()
    
    if season:
        season_df = season_df[season_df['Season'] == season]
    
    if league:
        season_df = season_df[season_df['League'] == league]
    
    standings = {}
    
    for _, match in season_df.iterrows():
        home_team = match['HomeTeam']
        away_team = match['AwayTeam']
        home_goals = match['FullTimeHomeGoals']
        away_goals = match['FullTimeAwayGoals']
        
        if pd.isna(home_team) or pd.isna(away_team):
            continue
        
        if home_team not in standings:
            standings[home_team] = {'Team': home_team, 'Played': 0, 'Won': 0, 'Drawn': 0, 'Lost': 0,
                                   'Goals For': 0, 'Goals Against': 0, 'Goal Difference': 0, 'Points': 0}
        if away_team not in standings:
            standings[away_team] = {'Team': away_team, 'Played': 0, 'Won': 0, 'Drawn': 0, 'Lost': 0,
                                   'Goals For': 0, 'Goals Against': 0, 'Goal Difference': 0, 'Points': 0}
        
        standings[home_team]['Played'] += 1
        standings[away_team]['Played'] += 1
        standings[home_team]['Goals For'] += home_goals
        standings[home_team]['Goals Against'] += away_goals
        standings[away_team]['Goals For'] += away_goals
        standings[away_team]['Goals Against'] += home_goals
        
        if home_goals > away_goals:
            standings[home_team]['Won'] += 1
            standings[home_team]['Points'] += 3
            standings[away_team]['Lost'] += 1
        elif home_goals < away_goals:
            standings[away_team]['Won'] += 1
            standings[away_team]['Points'] += 3
            standings[home_team]['Lost'] += 1
        else:
            standings[home_team]['Drawn'] += 1
            standings[away_team]['Drawn'] += 1
            standings[home_team]['Points'] += 1
            standings[away_team]['Points'] += 1
    
    standings_df = pd.DataFrame(standings.values())
    standings_df['Goal Difference'] = standings_df['Goals For'] - standings_df['Goals Against']
    standings_df = standings_df.sort_values(
        by=['Points', 'Goal Difference', 'Goals For'],
        ascending=[False, False, False]
    ).reset_index(drop=True)
    standings_df['Position'] = range(1, len(standings_df) + 1)
    
    column_order = ['Position', 'Team', 'Played', 'Won', 'Drawn', 'Lost', 
                   'Goals For', 'Goals Against', 'Goal Difference', 'Points']
    
    return standings_df[column_order]

# Example: Get Premier League 2023/24 standings
pl_table = calculate_league_standings(df, season='2023/24', league='Premier League')
```

## Update Schedule

- **Historical Data**: Static (2000/01 - 2024/25)
- **Current Season**: Updated after each matchday
- **Update Script**: Run `update_football_data.py` to fetch latest matches

## Data Source

Data sourced from [Football-Data.co.uk](https://www.football-data.co.uk/), a comprehensive football statistics platform providing historical match results and betting odds data since 1993.

## License & Attribution

This data is freely available from Football-Data.co.uk. When using this data, please acknowledge the source.

## File Size Estimates

- Historical (2000-2024): ~15-20 MB
- Current Season: ~500 KB
- Complete Dataset: ~20-25 MB

## Contact & Updates

For the latest data updates, run the provided Python script or visit Football-Data.co.uk directly.
