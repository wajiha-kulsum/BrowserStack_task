import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from deep_translator import GoogleTranslator


class ElPaisScraper:
    def __init__(self, driver=None):
        self.driver = driver if driver else webdriver.Chrome()
        self.base_url = "https://elpais.com/opinion/"
        self.articles_data = []
        self.images_dir = "article_images"
        
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
    
    def scrape_opinion_section(self):
        print("Navigating to El País Opinion section...")
        self.driver.get(self.base_url)
        
        time.sleep(3)
        
        try:
            cookie_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceptar') or contains(text(), 'Accept')]"))
            )
            cookie_button.click()
            print("Cookie consent accepted")
        except:
            print("No cookie consent found or already accepted")
        
        time.sleep(2)
        
        print("Fetching first 5 articles...")
        article_links = self.get_article_links()
        
        for idx, link in enumerate(article_links[:5], 1):
            print(f"\n{'='*80}")
            print(f"Processing Article {idx}/5")
            print(f"{'='*80}")
            article_data = self.scrape_article(link, idx)
            if article_data:
                self.articles_data.append(article_data)
        
        return self.articles_data
    
    def get_article_links(self):
        article_links = []
        
        try:
            articles = self.driver.find_elements(By.CSS_SELECTOR, "article h2 a, article h3 a, .c_h a")
            
            for article in articles[:10]:
                href = article.get_attribute('href')
                if href and '/opinion/' in href and href not in article_links:
                    article_links.append(href)
                    if len(article_links) >= 5:
                        break
            
            if not article_links:
                links = self.driver.find_elements(By.TAG_NAME, "a")
                for link in links:
                    href = link.get_attribute('href')
                    if href and '/opinion/' in href and href not in article_links:
                        article_links.append(href)
                        if len(article_links) >= 5:
                            break
        
        except Exception as e:
            print(f"Error getting article links: {e}")
        
        return article_links
    
    def scrape_article(self, url, idx):
        try:
            self.driver.get(url)
            time.sleep(2)
            
            article_data = {
                'url': url,
                'title': '',
                'content': '',
                'image_path': None
            }
            
            try:
                title_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "h1"))
                )
                article_data['title'] = title_element.text.strip()
            except:
                try:
                    title_element = self.driver.find_element(By.CSS_SELECTOR, ".a_t, .article-header h1, h1")
                    article_data['title'] = title_element.text.strip()
                except:
                    article_data['title'] = "Title not found"
            
            print(f"\nTitle (Spanish): {article_data['title']}")
            
            try:
                paragraphs = self.driver.find_elements(By.CSS_SELECTOR, "article p, .a_c p, .article-body p")
                content_parts = [p.text.strip() for p in paragraphs if p.text.strip() and len(p.text.strip()) > 50]
                article_data['content'] = '\n\n'.join(content_parts[:5])
                
                if article_data['content']:
                    print(f"\nContent (Spanish):\n{article_data['content'][:500]}...")
                else:
                    print("\nContent: Not available")
            except Exception as e:
                print(f"Error extracting content: {e}")
                article_data['content'] = "Content not available"
            
            try:
                image_selectors = [
                    "article img",
                    ".a_m img",
                    "figure img",
                    "img[src*='cloudfront']",
                    "img[src*='elpais']"
                ]
                
                image_element = None
                for selector in image_selectors:
                    try:
                        images = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for img in images:
                            src = img.get_attribute('src')
                            if src and ('cloudfront' in src or 'elpais' in src) and not src.endswith('.svg'):
                                image_element = img
                                break
                        if image_element:
                            break
                    except:
                        continue
                
                if image_element:
                    image_url = image_element.get_attribute('src')
                    if not image_url:
                        image_url = image_element.get_attribute('data-src')
                    
                    if image_url and image_url.startswith('http'):
                        image_path = self.download_image(image_url, idx)
                        article_data['image_path'] = image_path
                        print(f"Image downloaded: {image_path}")
                    else:
                        print("Image URL not valid")
                else:
                    print("No cover image found")
            except Exception as e:
                print(f"Error downloading image: {e}")
            
            return article_data
        
        except Exception as e:
            print(f"Error scraping article {url}: {e}")
            return None
    
    def download_image(self, image_url, idx):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(image_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                extension = 'jpg'
                if 'image/png' in response.headers.get('Content-Type', ''):
                    extension = 'png'
                elif 'image/jpeg' in response.headers.get('Content-Type', ''):
                    extension = 'jpg'
                
                filename = f"article_{idx}_cover.{extension}"
                filepath = os.path.join(self.images_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                return filepath
        except Exception as e:
            print(f"Failed to download image: {e}")
        
        return None
    
    def translate_headers(self):
        print(f"\n{'='*80}")
        print("TRANSLATED HEADERS")
        print(f"{'='*80}")
        
        translated_headers = []
        translator = GoogleTranslator(source='es', target='en')
        
        for idx, article in enumerate(self.articles_data, 1):
            try:
                translated = translator.translate(article['title'])
                translated_headers.append(translated)
                print(f"\nArticle {idx}:")
                print(f"Original (ES): {article['title']}")
                print(f"Translated (EN): {translated}")
            except Exception as e:
                print(f"Error translating article {idx}: {e}")
                translated_headers.append(article['title'])
        
        return translated_headers
    
    def analyze_word_frequency(self, translated_headers):
        print(f"\n{'='*80}")
        print("WORD FREQUENCY ANALYSIS")
        print(f"{'='*80}")
        
        all_words = []
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
                     'has', 'have', 'had', 'will', 'would', 'could', 'should', 'may', 'might'}
        
        for header in translated_headers:
            words = re.findall(r'\b[a-zA-Z]+\b', header.lower())
            filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
            all_words.extend(filtered_words)
        
        word_counts = Counter(all_words)
        repeated_words = {word: count for word, count in word_counts.items() if count > 2}
        
        if repeated_words:
            print("\nWords repeated more than twice:")
            for word, count in sorted(repeated_words.items(), key=lambda x: x[1], reverse=True):
                print(f"{word}: {count} occurrences")
        else:
            print("\nNo words repeated more than twice")
        
        return repeated_words
    
    def run(self):
        try:
            self.scrape_opinion_section()
            
            translated_headers = self.translate_headers()
            
            self.analyze_word_frequency(translated_headers)
            
            print(f"\n{'='*80}")
            print("SCRAPING COMPLETED SUCCESSFULLY")
            print(f"{'='*80}")
            print(f"Total articles scraped: {len(self.articles_data)}")
            print(f"Images saved in: {self.images_dir}/")
            
        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            if self.driver:
                self.driver.quit()


def main():
    print("El País Opinion Section Scraper")
    print("="*80)
    
    scraper = ElPaisScraper()
    scraper.run()


if __name__ == "__main__":
    main()
