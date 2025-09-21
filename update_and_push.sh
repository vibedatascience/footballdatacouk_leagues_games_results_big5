#!/bin/bash

# Football Data Auto-Update Script
# Runs daily to fetch latest matches and push to GitHub

cd /Users/rchaudhary/football-data.co.uk

# Log file for debugging
LOG_FILE="/Users/rchaudhary/football-data.co.uk/cron.log"
DATE=$(date "+%Y-%m-%d %H:%M:%S")

echo "[$DATE] Starting football data update..." >> $LOG_FILE

# Run the Python script to fetch latest data
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 latest.py >> $LOG_FILE 2>&1

# Check if Python script succeeded
if [ $? -eq 0 ]; then
    echo "[$DATE] Data update successful, pushing to GitHub..." >> $LOG_FILE
    
    # Add and commit changes
    /usr/bin/git add footballdatacouk_leagues_games_results_*_latest.csv footballdatacouk_leagues_games_results_2000_ytd.csv >> $LOG_FILE 2>&1
    
    # Only commit if there are changes
    if ! /usr/bin/git diff --cached --quiet; then
        /usr/bin/git commit -m "Auto-update: Football data $(date +%Y-%m-%d)" >> $LOG_FILE 2>&1
        /usr/bin/git push origin main >> $LOG_FILE 2>&1
        
        if [ $? -eq 0 ]; then
            echo "[$DATE] Successfully pushed to GitHub" >> $LOG_FILE
        else
            echo "[$DATE] ERROR: Failed to push to GitHub" >> $LOG_FILE
        fi
    else
        echo "[$DATE] No changes to commit" >> $LOG_FILE
    fi
else
    echo "[$DATE] ERROR: Python script failed" >> $LOG_FILE
fi

echo "[$DATE] Update process completed" >> $LOG_FILE
echo "----------------------------------------" >> $LOG_FILE
