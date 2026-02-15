@echo off
echo ================================================
echo Running El Pais Scraper Locally
echo ================================================
echo.

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Run the scraper
python elpais_scraper.py

echo.
echo ================================================
echo Scraping completed!
echo Check article_images/ folder for downloaded images
echo ================================================
pause
