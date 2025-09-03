# Football Data Column Descriptions

## 📅 MATCH INFORMATION
- **Div**: Division/League code (E0=Premier League, I1=Serie A, SP1=La Liga, G1=Bundesliga, F1=Ligue 1)
- **Date**: Match date (DD/MM/YYYY or YYYY-MM-DD format)
- **Time**: Kick-off time
- **HomeTeam**: Home team name
- **AwayTeam**: Away team name
- **HT**: Home team (abbreviated)
- **AT**: Away team (abbreviated)
- **Referee**: Match referee name
- **Attendance**: Number of spectators at the match
- **League**: Full league name (added column)
- **Season**: Season in YYYY/YY format (added column)

## ⚽ MATCH RESULTS
- **FTHG**: Full Time Home Goals
- **FTAG**: Full Time Away Goals
- **FTR**: Full Time Result (H=Home Win, D=Draw, A=Away Win)
- **HTHG**: Half Time Home Goals
- **HTAG**: Half Time Away Goals
- **HTR**: Half Time Result (H=Home Win, D=Draw, A=Away Win)

## 📊 MATCH STATISTICS
- **HS**: Home Shots
- **AS**: Away Shots
- **HST**: Home Shots on Target
- **AST**: Away Shots on Target
- **HF**: Home Fouls Committed
- **AF**: Away Fouls Committed
- **HC**: Home Corners
- **AC**: Away Corners
- **HY**: Home Yellow Cards
- **AY**: Away Yellow Cards
- **HR**: Home Red Cards
- **AR**: Away Red Cards
- **HO**: Home Offsides
- **AO**: Away Offsides
- **HHW**: Home Hit Woodwork
- **AHW**: Away Hit Woodwork
- **HFKC**: Home Fouls Committed (duplicate in some seasons)
- **AFKC**: Away Fouls Committed (duplicate in some seasons)

## 💰 BETTING ODDS

### Standard Betting Markets (1X2 - Match Result)
Each bookmaker typically has three columns:
- **[Bookmaker]H**: Home Win odds (e.g., B365H = Bet365 Home odds)
- **[Bookmaker]D**: Draw odds (e.g., B365D = Bet365 Draw odds)
- **[Bookmaker]A**: Away Win odds (e.g., B365A = Bet365 Away odds)

### Bookmaker Prefixes:
- **B365**: Bet365
- **BW**: Betwin
- **IW**: Interwetten
- **LB**: Ladbrokes
- **PS**: Pinnacle Sports
- **WH**: William Hill
- **SJ**: Stan James
- **VC**: VC Bet
- **GB**: Gamebookers
- **BS**: Blue Square
- **SY**: Stanleybet
- **SO**: Sporting Odds
- **BF**: Betfair
- **1XB**: 1xBet

### Over/Under 2.5 Goals Market
- **[Bookmaker]>2.5**: Odds for Over 2.5 goals (e.g., B365>2.5)
- **[Bookmaker]<2.5**: Odds for Under 2.5 goals (e.g., B365<2.5)

### Asian Handicap Markets
- **[Bookmaker]AHH**: Asian Handicap Home odds
- **[Bookmaker]AHA**: Asian Handicap Away odds
- **[Bookmaker]AH**: Asian Handicap size

### Closing Odds (C suffix)
- **[Bookmaker]CH**: Closing Home Win odds
- **[Bookmaker]CD**: Closing Draw odds
- **[Bookmaker]CA**: Closing Away Win odds
- **[Bookmaker]C>2.5**: Closing Over 2.5 goals odds
- **[Bookmaker]C<2.5**: Closing Under 2.5 goals odds
- **[Bookmaker]CAHH**: Closing Asian Handicap Home odds
- **[Bookmaker]CAHA**: Closing Asian Handicap Away odds

### Exchange Odds (Betfair)
- **BFH, BFD, BFA**: Betfair Exchange Home/Draw/Away odds
- **BFEH, BFED, BFEA**: Betfair Exchange (early) odds
- **BFCH, BFCD, BFCA**: Betfair Exchange closing odds
- **BFECH, BFECD, BFECA**: Betfair Exchange (early closing) odds

## 📈 BETTING AGGREGATES
- **Bb1X2**: Number of bookmakers offering 1X2 odds
- **BbMxH**: Maximum Home Win odds
- **BbAvH**: Average Home Win odds
- **BbMxD**: Maximum Draw odds
- **BbAvD**: Average Draw odds
- **BbMxA**: Maximum Away Win odds
- **BbAvA**: Average Away Win odds
- **BbOU**: Number of bookmakers offering Over/Under odds
- **BbMx>2.5**: Maximum Over 2.5 goals odds
- **BbAv>2.5**: Average Over 2.5 goals odds
- **BbMx<2.5**: Maximum Under 2.5 goals odds
- **BbAv<2.5**: Average Under 2.5 goals odds
- **BbAH**: Number of bookmakers offering Asian Handicap
- **BbAHh**: Asian Handicap size (market average)
- **BbMxAHH**: Maximum Asian Handicap Home odds
- **BbAvAHH**: Average Asian Handicap Home odds
- **BbMxAHA**: Maximum Asian Handicap Away odds
- **BbAvAHA**: Average Asian Handicap Away odds

### Market Aggregates
- **MaxH, MaxD, MaxA**: Maximum odds across all bookmakers
- **AvgH, AvgD, AvgA**: Average odds across all bookmakers
- **Max>2.5, Max<2.5**: Maximum Over/Under 2.5 goals odds
- **Avg>2.5, Avg<2.5**: Average Over/Under 2.5 goals odds
- **P>2.5, P<2.5**: Pinnacle Over/Under 2.5 goals odds
- **PC>2.5, PC<2.5**: Pinnacle Closing Over/Under 2.5 goals odds
- **PAHH, PAHA**: Pinnacle Asian Handicap odds
- **PCAHH, PCAHA**: Pinnacle Closing Asian Handicap odds

## Notes:
- Not all columns appear in every season (data availability varies)
- Betting odds are decimal format (European odds)
- Some columns may be empty for certain matches or seasons
- "Unnamed" columns are typically empty or contain metadata