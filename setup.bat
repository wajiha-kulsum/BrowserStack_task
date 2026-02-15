@echo off
echo ================================================
echo Setting up El Pais Scraper Project
echo ================================================
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Create directories
echo Creating required directories...
if not exist article_images mkdir article_images

echo.
echo ================================================
echo Setup completed successfully!
echo ================================================
echo.
echo Next steps:
echo 1. Set BrowserStack credentials (if testing on BrowserStack):
echo    set BROWSERSTACK_USERNAME=your_username
echo    set BROWSERSTACK_ACCESS_KEY=your_access_key
echo.
echo 2. Run locally: run_local.bat
echo 3. Run on BrowserStack: run_browserstack.bat
echo.
pause
