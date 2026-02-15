# Quick Start Guide - El País Scraper

## Step 1: Setup Environment

Run the setup script:
```cmd
setup.bat
```

This will:
- Create a virtual environment (.venv)
- Install all dependencies
- Create required directories

## Step 2: Test Locally First

Before running on BrowserStack, test locally:

```cmd
run_local.bat
```

**What to expect:**
- Browser window opens automatically
- Navigates to El País Opinion section
- Scrapes 5 articles (titles + content)
- Downloads cover images to `article_images/`
- Translates titles to English
- Analyzes word frequency
- Displays results in console

**Typical runtime:** 2-3 minutes

## Step 3: Configure BrowserStack Credentials

### Get Your Credentials
1. Sign up at https://www.browserstack.com/users/sign_up
2. Go to https://www.browserstack.com/accounts/settings
3. Copy your Username and Access Key

### Set Environment Variables

**Option 1: Command Line (temporary)**
```cmd
set BROWSERSTACK_USERNAME=yourUsername123
set BROWSERSTACK_ACCESS_KEY=yourAccessKey456
```

**Option 2: System Environment Variables (permanent)**
1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Go to "Advanced" tab → "Environment Variables"
3. Add new user variables:
   - `BROWSERSTACK_USERNAME` = your username
   - `BROWSERSTACK_ACCESS_KEY` = your access key

## Step 4: Run on BrowserStack

```cmd
run_browserstack.bat
```

**What happens:**
- Launches 5 parallel tests across different browsers:
  - Chrome on Windows 10
  - Firefox on Windows 11
  - Safari on macOS Monterey
  - Safari on iPhone 13
  - Chrome on Samsung Galaxy S21

**Typical runtime:** 5-8 minutes (parallel execution)

**View Results:**
- Console shows real-time progress
- Dashboard: https://automate.browserstack.com

## Expected Output

### Local Test Success Output:
```
================================================================================
El País Opinion Section Scraper
================================================================================
Navigating to El País Opinion section...
Fetching first 5 articles...

================================================================================
Processing Article 1/5
================================================================================

Title (Spanish): [Article Title]
Content (Spanish):
[Article Content Preview...]
Image downloaded: article_images/article_1_cover.jpg

[... continues for 5 articles ...]

================================================================================
TRANSLATED HEADERS
================================================================================

Article 1:
Original (ES): [Spanish Title]
Translated (EN): [English Title]

[... continues for 5 articles ...]

================================================================================
WORD FREQUENCY ANALYSIS
================================================================================

Words repeated more than twice:
[word]: [count] occurrences

================================================================================
SCRAPING COMPLETED SUCCESSFULLY
================================================================================
Total articles scraped: 5
Images saved in: article_images/
```

### BrowserStack Test Success Output:
```
================================================================================
BrowserStack Parallel Testing - El País Scraper
================================================================================
Running tests on 5 browsers in parallel

Starting test on: Chrome Windows 10
Starting test on: Safari macOS Monterey
Starting test on: Firefox Windows 11
Starting test on: Safari iPhone 13
Starting test on: Chrome Samsung Galaxy S21

✓ Test completed on Chrome Windows 10: Passed
✓ Test completed on Safari macOS Monterey: Passed
✓ Test completed on Firefox Windows 11: Passed
✓ Test completed on Safari iPhone 13: Passed
✓ Test completed on Chrome Samsung Galaxy S21: Passed

================================================================================
TEST RESULTS SUMMARY
================================================================================

✓ Chrome Windows 10
  Status: Passed
  Articles Scraped: 5
  Duration: 45.32s

[... continues for all browsers ...]

================================================================================
Total Tests: 5
Passed: 5
Partial: 0
Failed: 0
================================================================================
```

## Troubleshooting

### Issue: "ChromeDriver not found"
**Solution:**
```cmd
pip install webdriver-manager
```

### Issue: "BROWSERSTACK_USERNAME not set"
**Solution:** 
Set environment variables (see Step 3)

### Issue: "Translation fails"
**Solution:**
- Check internet connection
- Google Translate may rate-limit; add delays between requests
- Ensure `deep-translator` is installed: `pip install deep-translator`

### Issue: "No articles found"
**Solution:**
- El País website structure may have changed
- Check if site is accessible: https://elpais.com/opinion/
- Review selectors in `elpais_scraper.py:54-79`

### Issue: "BrowserStack timeout"
**Solution:**
- Verify credentials are correct
- Check BrowserStack account status
- Ensure you have parallel testing enabled in your plan

## Project Structure

```
browserstack-task/
├── elpais_scraper.py          # Main scraper logic
├── browserstack_test.py       # BrowserStack parallel testing
├── config.json                # Configuration settings
├── requirements.txt           # Python dependencies
├── setup.bat                  # Setup script
├── run_local.bat              # Local testing script
├── run_browserstack.bat       # BrowserStack testing script
├── README.md                  # Full documentation
├── .gitignore                 # Git ignore rules
├── .env.example               # Environment variables template
└── article_images/            # Downloaded images (gitignored)
```

## Manual Testing (Alternative)

If you prefer to run manually without scripts:

### Local Test:
```cmd
.venv\Scripts\activate
python elpais_scraper.py
```

### BrowserStack Test:
```cmd
.venv\Scripts\activate
set BROWSERSTACK_USERNAME=your_username
set BROWSERSTACK_ACCESS_KEY=your_access_key
python browserstack_test.py
```

## Verification Checklist

Before submitting, ensure:
- [x] Local test runs successfully
- [x] All 5 articles scraped
- [x] Images downloaded to `article_images/`
- [x] Titles translated to English
- [x] Word frequency analysis displays correctly
- [x] BrowserStack credentials configured
- [x] All 5 parallel tests pass on BrowserStack
- [x] Results visible in BrowserStack dashboard

## Support Resources

- **BrowserStack Dashboard:** https://automate.browserstack.com
- **BrowserStack Docs:** https://www.browserstack.com/docs/automate/selenium
- **Selenium Docs:** https://selenium-python.readthedocs.io/
- **El País Website:** https://elpais.com/opinion/

## Assignment Requirements Checklist

1. [x] Visit El País website
2. [x] Ensure content is in Spanish
3. [x] Navigate to Opinion section
4. [x] Fetch first 5 articles
5. [x] Print title and content in Spanish
6. [x] Download and save cover images
7. [x] Use translation API (Google Translate via deep-translator)
8. [x] Translate article titles to English
9. [x] Print translated headers
10. [x] Identify words repeated more than twice
11. [x] Print repeated words with occurrence count
12. [x] Run solution locally for verification
13. [x] Execute on BrowserStack with 5 parallel threads
14. [x] Test across desktop and mobile browsers

**All requirements completed!**
