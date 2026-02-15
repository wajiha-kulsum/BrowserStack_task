@echo off
echo ================================================
echo Running El Pais Scraper on BrowserStack
echo ================================================
echo.

REM Check if environment variables are set
if "%BROWSERSTACK_USERNAME%"=="" (
    echo ERROR: BROWSERSTACK_USERNAME not set
    echo.
    echo Please set your BrowserStack credentials:
    echo set BROWSERSTACK_USERNAME=your_username
    echo set BROWSERSTACK_ACCESS_KEY=your_access_key
    echo.
    pause
    exit /b 1
)

if "%BROWSERSTACK_ACCESS_KEY%"=="" (
    echo ERROR: BROWSERSTACK_ACCESS_KEY not set
    echo.
    echo Please set your BrowserStack credentials:
    echo set BROWSERSTACK_USERNAME=your_username
    echo set BROWSERSTACK_ACCESS_KEY=your_access_key
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Run the BrowserStack tests
python browserstack_test.py

echo.
echo ================================================
echo BrowserStack tests completed!
echo Check https://automate.browserstack.com for test results
echo ================================================
pause
