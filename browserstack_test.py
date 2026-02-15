import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from elpais_scraper import ElPaisScraper


BROWSERSTACK_USERNAME = os.getenv('BROWSERSTACK_USERNAME', 'your_username')
BROWSERSTACK_ACCESS_KEY = os.getenv('BROWSERSTACK_ACCESS_KEY', 'your_access_key')
BROWSERSTACK_URL = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"


BROWSER_CONFIGS = [
    {
        'os': 'Windows',
        'os_version': '10',
        'browser': 'Chrome',
        'browser_version': 'latest',
        'name': 'Chrome Windows 10'
    },
    {
        'os': 'OS X',
        'os_version': 'Monterey',
        'browser': 'Safari',
        'browser_version': 'latest',
        'name': 'Safari macOS Monterey'
    },
    {
        'os': 'Windows',
        'os_version': '11',
        'browser': 'Firefox',
        'browser_version': 'latest',
        'name': 'Firefox Windows 11'
    },
    {
        'device': 'iPhone 13',
        'os_version': '15',
        'browser': 'Safari',
        'real_mobile': 'true',
        'name': 'Safari iPhone 13'
    },
    {
        'device': 'Samsung Galaxy S21',
        'os_version': '11.0',
        'browser': 'Chrome',
        'real_mobile': 'true',
        'name': 'Chrome Samsung Galaxy S21'
    }
]


def create_browserstack_driver(config):
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    
    options = ChromeOptions()
    
    # BrowserStack specific options
    bstack_options = {
        'userName': BROWSERSTACK_USERNAME,
        'accessKey': BROWSERSTACK_ACCESS_KEY,
        'projectName': 'El Pais Scraper',
        'buildName': 'v1.0',
        'sessionName': config.get('name', 'Test'),
        'debug': 'true',
        'consoleLogs': 'verbose',
        'networkLogs': 'true'
    }
    
    # Add OS and browser configuration
    if 'os' in config:
        bstack_options['os'] = config['os']
        bstack_options['osVersion'] = config.get('os_version', '')
    if 'device' in config:
        bstack_options['deviceName'] = config['device']
        bstack_options['osVersion'] = config.get('os_version', '')
        bstack_options['realMobile'] = config.get('real_mobile', 'true')
    if 'browser' in config:
        bstack_options['browserName'] = config['browser']
        bstack_options['browserVersion'] = config.get('browser_version', 'latest')
    
    options.set_capability('bstack:options', bstack_options)
    
    driver = webdriver.Remote(
        command_executor=BROWSERSTACK_URL,
        options=options
    )
    
    return driver


def run_test_on_browser(config):
    driver = None
    test_result = {
        'browser': config.get('name', 'Unknown'),
        'status': 'Failed',
        'articles_scraped': 0,
        'error': None,
        'start_time': time.time()
    }
    
    try:
        print(f"\nStarting test on: {config.get('name')}")
        
        driver = create_browserstack_driver(config)
        
        scraper = ElPaisScraper(driver=driver)
        
        scraper.scrape_opinion_section()
        
        test_result['articles_scraped'] = len(scraper.articles_data)
        
        if len(scraper.articles_data) >= 3:
            test_result['status'] = 'Passed'
        else:
            test_result['status'] = 'Partial'
        
        translated_headers = scraper.translate_headers()
        scraper.analyze_word_frequency(translated_headers)
        
        print(f"[PASS] Test completed on {config.get('name')}: {test_result['status']}")
        
    except Exception as e:
        test_result['error'] = str(e)
        print(f"[FAIL] Test failed on {config.get('name')}: {e}")
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        
        test_result['duration'] = time.time() - test_result['start_time']
    
    return test_result


def run_parallel_tests():
    print("="*80)
    print("BrowserStack Parallel Testing - El País Scraper")
    print("="*80)
    print(f"Running tests on {len(BROWSER_CONFIGS)} browsers in parallel\n")
    
    results = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(run_test_on_browser, config): config for config in BROWSER_CONFIGS}
        
        for future in as_completed(futures):
            config = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Exception for {config.get('name')}: {e}")
                results.append({
                    'browser': config.get('name'),
                    'status': 'Failed',
                    'error': str(e),
                    'articles_scraped': 0
                })
    
    print("\n" + "="*80)
    print("TEST RESULTS SUMMARY")
    print("="*80)
    
    passed = sum(1 for r in results if r['status'] == 'Passed')
    failed = sum(1 for r in results if r['status'] == 'Failed')
    partial = sum(1 for r in results if r['status'] == 'Partial')
    
    for result in results:
        status_symbol = "[PASS]" if result['status'] == 'Passed' else "[FAIL]"
        print(f"\n{status_symbol} {result['browser']}")
        print(f"  Status: {result['status']}")
        print(f"  Articles Scraped: {result['articles_scraped']}")
        if result.get('duration'):
            print(f"  Duration: {result['duration']:.2f}s")
        if result.get('error'):
            print(f"  Error: {result['error']}")
    
    print("\n" + "="*80)
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Partial: {partial}")
    print(f"Failed: {failed}")
    print("="*80)
    
    return results


def main():
    if BROWSERSTACK_USERNAME == 'your_username' or BROWSERSTACK_ACCESS_KEY == 'your_access_key':
        print("\nWARNING: Please set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY environment variables")
        print("\nExample:")
        print("  export BROWSERSTACK_USERNAME='your_username'")
        print("  export BROWSERSTACK_ACCESS_KEY='your_access_key'")
        print("\nOr set them in your script directly (not recommended for production)")
        return
    
    run_parallel_tests()


if __name__ == "__main__":
    main()
