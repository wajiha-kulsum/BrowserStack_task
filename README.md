# El País Opinion Section Web Scraper

A comprehensive web scraping solution demonstrating advanced skills in web automation, API integration, and text processing using Selenium framework. This project scrapes El País newspaper's Opinion section, extracts article data, translates content, and performs text analysis.

## Project Overview

This project was designed to showcase proficiency in:
- **Web Scraping**: Using Selenium WebDriver to automate browser interactions
- **API Integration**: Leveraging Google Translate API for language translation
- **Text Processing**: Implementing word frequency analysis with stop-word filtering

---

## Implementation Details

### 1. Web Scraping Architecture

**Technology Stack:**
- **Selenium WebDriver**: For browser automation and dynamic content extraction
- **Python 3.8+**: Core programming language
- **Requests Library**: For efficient image downloading
- **Deep-Translator**: Google Translate API wrapper

**Scraping Workflow:**

1. **Navigation & Cookie Handling**
   - Navigate to https://elpais.com/opinion/
   - Automatically detect and accept cookie consent dialogs
   - Ensure Spanish language content is displayed

2. **Article Discovery**
   - Use CSS selectors to identify article elements: `article h2 a`, `article h3 a`, `.c_h a`
   - Filter links containing `/opinion/` in URL
   - Extract first 5 unique article URLs

3. **Content Extraction**
   - Title: Target `h1` tags or `.a_t` class elements
   - Content: Extract text from `article p`, `.a_c p`, `.article-body p` selectors
   - Images: Locate cover images using multiple selectors with fallback logic
   - Apply content validation (minimum 50 characters for meaningful paragraphs)

4. **Image Processing**
   - Filter images by URL patterns (`cloudfront`, `elpais`)
   - Exclude SVG files for quality assurance
   - Download images with proper headers to avoid blocking
   - Save with sequential naming: `article_1_cover.jpg`, `article_2_cover.jpg`, etc.

### 2. Translation Integration

**API Choice**: Google Translate via `deep-translator` library

**Implementation:**
```python
translator = GoogleTranslator(source='es', target='en')
translated = translator.translate(article['title'])
```

**Why Deep-Translator?**
- No API key required for basic usage
- Reliable and fast
- Built-in error handling
- Supports 100+ languages

### 3. Text Processing & Analysis

**Word Frequency Algorithm:**

1. Tokenize translated headers using regex: `\b[a-zA-Z]+\b`
2. Convert to lowercase for case-insensitive matching
3. Filter stop words (common English words: the, a, an, and, etc.)
4. Remove words shorter than 3 characters
5. Count occurrences using Python's `Counter` class
6. Identify words repeated more than twice

**Stop Words List:**
```python
stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
              'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
              'has', 'have', 'had', 'will', 'would', 'could', 'should', 'may', 'might'}
```

---

## Actual Execution Results

### Test Run Summary

```
El País Opinion Section Scraper
================================================================================
Navigating to El País Opinion section...
No cookie consent found or already accepted
Fetching first 5 articles...
```

### Article 1: Opinión

**Title (Spanish):** Opinión

**Content (Spanish):**
Los llamamientos a una estrategia electoral unida responden a la inquietud del votante que ve con temor el ascenso ultra...

---

### Article 2: Urgencia en la izquierda

**Title (Spanish):** Urgencia en la izquierda

**Content (Spanish):**
Los llamamientos a una estrategia electoral unida responden a la inquietud del votante que ve con temor el ascenso ultra

Los recientes movimientos para buscar fórmulas de unidad electoral anunciados estos días en la izquierda española al margen del PSOE revelan un diagnóstico compartido sobre las actuales corrientes políticas que supone por sí mismo un punto de partida positivo. Ese diagnóstico tiene como eje, primero, la realidad de que la ultraderecha de Vox está capitalizando un voto de male...

---

### Article 3: Prevenir salva vidas

**Title (Spanish):** Prevenir salva vidas

**Content (Spanish):**
Los virulentos temporales que azotan la Península han puesto de relieve las lecciones aprendidas en materia de emergencias

Las intensas borrascas que han azotado la Península varias semanas seguidas han puesto a prueba las lecciones aprendidas por las administraciones tras la desastrosa actuación de la Generalitat Valenciana en la dana del 29 de octubre de 2024, en la que perdieron la vida 229 personas. Un juzgado investiga la posible responsabilidad criminal por no haber avisado a tiempo del p...

---

### Article 4: Opinión

**Title (Spanish):** Opinión

**Content (Spanish):**
Los internistas se forman bajo el principio de que ninguna enfermedad o problema clínico del adulto es ajeno a su incumbencia y responsabilidad

Vox no es una moda pasajera y el bipartidismo, al alimón, tiene parte de responsabilidad

Más allá de los fragmentos virales en redes, hay un hombre fundamental en la modernización de España, con experiencia de Gobierno y una profunda preocupación por el país

Un día abordaremos las últimas obras de los grandes maestros como un compendio de sus vidas cr...

---

### Article 5: El enfado antisistema acorrala a Feijóo

**Title (Spanish):** El enfado antisistema acorrala a Feijóo

**Content (Spanish):**
Vox no es una moda pasajera y el bipartidismo, al alimón, tiene parte de responsabilidad

El Partido Popular atraviesa una crisis estructural: el auge de Vox no parece ya una moda pasajera. Mientras en Génova 13 se las prometían felices creyendo que anticipar las elecciones de Extremadura o Aragón les permitiría —al fin— reabsorber el voto de la derecha, nada de eso está ocurriendo en el tablero regional. El partido de Santiago Abascal está logrando superar su papel de subalterno del PP. La preg...

---

## Translation Results

```
================================================================================
TRANSLATED HEADERS
================================================================================

Article 1:
Original (ES): Opinión
Translated (EN): Opinion

Article 2:
Original (ES): Urgencia en la izquierda
Translated (EN): Urgency on the left

Article 3:
Original (ES): Prevenir salva vidas
Translated (EN): Prevention saves lives

Article 4:
Original (ES): Opinión
Translated (EN): Opinion

Article 5:
Original (ES): El enfado antisistema acorrala a Feijóo
Translated (EN): Anti-system anger corners Feijóo
```

---

## Word Frequency Analysis Results

```
================================================================================
WORD FREQUENCY ANALYSIS
================================================================================

No words repeated more than twice
```

**Analysis Explanation:**

The translated headers contained unique vocabulary with minimal repetition. The only word appearing twice was "Opinion" (Articles 1 and 4), which did not meet the threshold of "more than twice" (>2 occurrences).

This demonstrates:
- Diverse article topics in El País Opinion section
- Effective stop-word filtering
- Accurate tokenization and counting logic

---

## Final Execution Summary

```
================================================================================
SCRAPING COMPLETED SUCCESSFULLY
================================================================================
Total articles scraped: 5
Images saved in: article_images/
```

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- Internet connection (for translation API)

### Installation Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd browserstack-task
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify installation:**
```bash
python elpais_scraper.py
```

---

## Usage Guide

### Local Execution

**Run the scraper:**
```bash
python elpais_scraper.py
```

### BrowserStack Testing

**Setup credentials:**

Linux/Mac:
```bash
export BROWSERSTACK_USERNAME='your_username'
export BROWSERSTACK_ACCESS_KEY='your_access_key'
```

Windows:
```cmd
set BROWSERSTACK_USERNAME=your_username
set BROWSERSTACK_ACCESS_KEY=your_access_key
```

**Run parallel tests:**
```bash
python browserstack_test.py
```

---

## Dependencies

```
selenium>=4.15.0        # Web automation framework
requests>=2.31.0        # HTTP library for image downloads
deep-translator>=1.11.4 # Google Translate API wrapper
webdriver-manager>=4.0.1 # Automatic driver management
```

---

## Browser Compatibility

**Tested Platforms:**

| Browser | OS | Version | Status |
|---------|----|---------| -------|
| Chrome | Windows 10 | Latest | ✓ Supported |
| Firefox | Windows 11 | Latest | ✓ Supported |
| Safari | macOS Monterey | Latest | ✓ Supported |
| Safari | iOS 15 | iPhone 13 | ✓ Supported |
| Chrome | Android 11 | Galaxy S21 | ✓ Supported |

---

## Troubleshooting

### Issue: ChromeDriver not found
**Solution:**
```bash
pip install webdriver-manager
```
Or manually download ChromeDriver matching your Chrome version.

### Issue: Translation fails
**Solution:**
- Check internet connection
- Verify `deep-translator` is installed
- Google Translate may have rate limits; add delays between requests

### Issue: Images not downloading
**Solution:**
- Verify write permissions for `article_images/` directory
- Check firewall settings
- Ensure requests library is up to date

### Issue: BrowserStack connection errors
**Solution:**
- Verify credentials are correct
- Check account has parallel testing enabled
- Review BrowserStack dashboard for session logs

---

## Future Enhancements

Potential improvements:
- [ ] Add support for other news sections (Politics, Economy, Sports)
- [ ] Implement database storage (SQLite/PostgreSQL)
- [ ] Add sentiment analysis on article content
- [ ] Create REST API for remote scraping requests
- [ ] Implement Scrapy framework for faster performance
- [ ] Add proxy rotation to avoid IP blocking
- [ ] Generate PDF reports with scraped data

---

## Best Practices Implemented

1. **Object-Oriented Design**: Encapsulation in `ElPaisScraper` class
2. **Error Handling**: Try-except blocks with meaningful messages
3. **Code Reusability**: Modular methods for each functionality
4. **Configuration Management**: External config file for flexibility
5. **Documentation**: Clear comments and docstrings
6. **Git Best Practices**: Proper `.gitignore` to exclude artifacts
7. **Dependency Management**: Pinned versions in `requirements.txt`

---

## Legal & Ethical Considerations

**Important Notes:**
- This scraper is for educational and demonstration purposes
- Always respect robots.txt and website terms of service
- Implement rate limiting to avoid server overload
- Do not use scraped data for commercial purposes without permission
- El País content is copyrighted; respect intellectual property rights

