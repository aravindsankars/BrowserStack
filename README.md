# Web Scraper and BrowserStack Testing Project

This repository contains a web scraping solution for extracting articles from the Opinion section of the Spanish news website **El País**. It includes functionality for translating article titles, analyzing translated headers, and testing the solution on multiple browsers using BrowserStack.

---

## Features
1. **Web Scraping**:
   - Extract the first five articles from the Opinion section of **El País**.
   - Print article titles and content in Spanish.
   - Download cover images of articles (if available).

2. **Translation**:
   - Use the **Rapid Translate Multi Traduction API** to translate article titles into English.
   - Identify repeated words across translated headers.

3. **Cross-Browser Testing**:
   - Validate functionality locally.
   - Execute the solution on **BrowserStack** with 5 parallel threads across various desktop and mobile browsers.

---

## Requirements
The following Python libraries are required:
- `selenium`
- `requests`
- `beautifulsoup4`
- `pillow`
- `browserstack-local>=1.2.3`
- `google-cloud-translate`
- `browserstack-sdk`

Install these dependencies from the `requirements.txt` file.

---

## Setup and Execution

### 1. Clone the Repository
Clone this repository to your local machine.

### 2. Create a Virtual Environment
Create and activate a Python virtual environment.

### 3. Install Dependencies
Install the required Python libraries.

### 4. Configuration Files
The project requires two YAML configuration files:

*secrets.yml: Store sensitive credentials like API keys.*
  
*browserstack.yml: Define BrowserStack testing configurations.*

### 5. Run the Local Scraper
Execute the local scraper to fetch articles, translate titles, and analyze headers:

**python src/main.py**

### 6. Run Cross-Browser Testing with BrowserStack
Run the solution on BrowserStack with parallel threads:

**python src_bs/main.py**

### Expected Output
#### Local Execution:

- Titles and content of the first five articles in Spanish.
- Cover images saved to the article_images folder.
- Translated titles in English.
- List of repeated words across headers with their counts.

#### BrowserStack Testing:

- Same functionality tested across different browser-device combinations in parallel.

### Notes
- Ensure the El País website is accessible and the Opinion section is available in Spanish.
- Replace placeholder values in secrets.yml with valid credentials for Rapid Translate API and BrowserStack.
- Test locally before executing BrowserStack tests to ensure functionality.

### Troubleshooting
*Dependency Issues:*

Ensure Python 3.x is installed and configured correctly.
Use pip freeze to verify all dependencies are installed.

*BrowserStack Issues:*

Check the browserstack.yml file for correct credentials and platform configurations.
Ensure browserstack-local and browserstack-sdk are installed.

*API Errors:*

Verify the Rapid Translate API key and URL in secrets.yml.
Check rate limits and usage for the API.
