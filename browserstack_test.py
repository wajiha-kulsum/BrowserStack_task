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
    desired_cap = {
        'browserstack.user': BROWSERSTACK_USERNAME,
        'browserstack.key': BROWSERSTACK_ACCESS_KEY,
        'project': 'El Pais Scraper',
        'build': 'v1.0',
        'name': config.get('name', 'Test'),
        'browserstack.debug': 'true',
        'browserstack.console': 'verbose',
        'browserstack.networkLogs': 'true'
    }
    
    desired_cap.update(config)
    
    driver = webdriver.Remote(
        command_executor=BROWSERSTACK_URL,
        desired_capabilities=desired_cap
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
        
        print(f"✓ Test completed on {config.get('name')}: {test_result['status']}")
        
    except Exception as e:
        test_result['error'] = str(e)
        print(f"✗ Test failed on {config.get('name')}: {e}")
    
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
        status_symbol = "✓" if result['status'] == 'Passed' else "✗"
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
        print("\n⚠ WARNING: Please set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY environment variables")
        print("\nExample:")
        print("  export BROWSERSTACK_USERNAME='your_username'")
        print("  export BROWSERSTACK_ACCESS_KEY='your_access_key'")
        print("\nOr set them in your script directly (not recommended for production)")
        return
    
    run_parallel_tests()


if __name__ == "__main__":
    main()
