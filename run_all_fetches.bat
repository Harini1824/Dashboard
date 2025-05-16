@echo off
echo Starting data fetch...

REM Run weather API script
python "C:\Users\Harini\dataproject\scripts\fetch_weather.py"

REM Run news API script
python "C:\Users\Harini\dataproject\scripts\fetch_news.py"

REM Run JSONPlaceholder script
python "C:\Users\Harini\dataproject\scripts\fetch_posts.py"

echo All scripts executed successfully.
pause
