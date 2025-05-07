import time
import pandas as pd
import requests
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#different query terms for wider range of articles
SEARCH_QUERIES = [
    "Ozempic",
    "Ozempic weight loss",
    "Ozempic shortage",
    "Ozempic FDA approval",
    "Ozempic side effects",
    "Wegovy and Ozempic"
]

NEWS_SOURCES = ["google", "bing", "msn"]


def setup_driver(): #sets up a headless chrome driver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

#paginations for different news search engines
def get_google_news_links(query, max_articles=50):
    driver = setup_driver()
    base_url = "https://www.google.com/search?q={}&tbm=nws&start={}"
    articles = set()
    
    for start in range(0, 50, 10):  # Paginate through first 5 pages
        search_url = base_url.format(query.replace(" ", "+"), start)
        driver.get(search_url)
        time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for link in soup.select("a.WlydOe"):  # Google News article links
            url = link["href"]
            if url.startswith("http") and "google.com" not in url:
                articles.add(url)
            if len(articles) >= max_articles:
                break

    driver.quit()
    return list(articles)


def get_bing_news_links(query, max_articles=50):
    driver = setup_driver()
    search_url = f"https://www.bing.com/news/search?q={query.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = set()

    for link in soup.select("a.title"):
        url = link["href"]
        if url.startswith("http"):
            articles.add(url)
        if len(articles) >= max_articles:
            break

    driver.quit()
    return list(articles)


def get_msn_news_links(query, max_articles=50):
    driver = setup_driver()
    search_url = f"https://www.msn.com/en-us/news/search?q={query.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = set()

    for link in soup.select("a[href]"):
        url = link["href"]
        if url.startswith("http") and "msn.com" in url:
            articles.add(url)
        if len(articles) >= max_articles:
            break

    driver.quit()
    return list(articles)


def clean_text(text):
    #some basic preprocessing
    text_lines = text.split("\n")
    filtered_lines = [
        line for line in text_lines
        if len(line) > 30 and not any(kw in line.lower() for kw in ["subscribe", "gifted", "premium", "credit card"])
    ]
    return " ".join(filtered_lines)


def scrape_article(url):
    #main parsing logic for the scraper
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        #title
        title = soup.find("title").text.strip() if soup.find("title") else "No Title"

        # Extract paragraphs from <article> tag if available
        article_tag = soup.find("article")  
        if article_tag:
            paragraphs = article_tag.find_all("p")
        else:
            paragraphs = soup.find_all("p")

        text = clean_text(" ".join([p.text.strip() for p in paragraphs]))

        return title, url, text
    except Exception as e:
        logging.error(f"Failed to scrape {url}: {e}")
        return None, url, None


def main():
    all_articles = set()  #avoids duplicate articles
    data = []

    for query in SEARCH_QUERIES:
        logging.info(f"Scraping news articles for topic: {query}")

        #getting links from different sources due to different limits on different news search engines
        google_links = get_google_news_links(query, max_articles=50)
        bing_links = get_bing_news_links(query, max_articles=50)
        msn_links = get_msn_news_links(query, max_articles=50)

        for url in google_links + bing_links + msn_links:
            if url not in all_articles:
                logging.info(f"Scraping article: {url}")
                title, url, text = scrape_article(url)
                if text:
                    data.append([title, url, text])
                    all_articles.add(url)

            #150 is good enough
            if len(all_articles) >= 150:
                break

    df = pd.DataFrame(data, columns=["Title", "URL", "Text"])
    df.to_csv("ozempic_news_150.csv", index=False)
    logging.info(f"Scraping complete. {len(df)} articles saved to ozempic_news_150.csv")


if __name__ == "__main__":
    main()
