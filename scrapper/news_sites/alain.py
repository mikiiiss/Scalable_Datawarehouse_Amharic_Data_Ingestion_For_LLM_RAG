from enum import Enum
import re
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

url = f"https://am.al-ain.com/"

number_of_pages_to_scrape = 1

class AlainNewsCategory(Enum):
    POLITICS = 'politics'
    SOCIAL = 'social'
    ECONOMY = 'economy'
    VARIETIES = 'varieties'
    SPORT = 'sport'

class AlainNewsButton(Enum):    
    LOADING = "ተጨማሪ ጫን"
    NEXT_PAGE = 'next page'

def scroll_down(driver: webdriver.Chrome, timeout: int = 10):
    """
    This function scrolls down to the end of the page using the execute_script method
    of the webdriver object. This function also has a timeout argument which is the
    time in seconds to wait until the page is scrolled down. The default value of
    this argument is 10 second.
    """
    # This function use the execute_script method to scroll down to the end of the
    # page. The JavaScript code is similar to the previous one, the difference is
    # that this time we are using the argument "arguments[0]" to pass the timeout
    # to the code and wait until the scroll is done.
    driver.execute_script(
        "var start = performance.now(); var end = start + arguments[0]; while (performance.now() < end) { window.scrollTo(0, document.body.scrollHeight); }",
        timeout
    )

def initialize_driver(url: str, category: AlainNewsCategory) -> None:
    
    full_url = f"{url}/section/{category.value}/"

    driver.get(full_url)

def get_all_articles_on_page_by_category(driver: webdriver.Chrome) -> list[WebElement]:

    # Scroll down
    scroll_down(driver)

    # Get the next page button
    next_page = get_next_page_element(driver)

    # Check until the next page button is available which changes from "ተጨማሪ ጫን" to "next page"
    while next_page.text == AlainNewsButton.LOADING:
        next_page = get_next_page_element(driver)

    # Now we have got all the pages loaded with all possible articles    
    articles = get_articles_element(driver)

    return articles

def get_articles_element(driver: webdriver.Chrome) -> list[WebElement]:
    return driver.find_element(By.XPATH, '//div[@class="row loadmore"]').find_elements(By.TAG_NAME, 'article')

def get_next_page_element(driver: webdriver.Chrome) -> WebElement:
    return driver.find_elements(By.TAG_NAME, 'footer')[0].find_element(By.TAG_NAME, 'a')

def get_image_url(article: WebElement) -> str:
    """Return the srcset attribute of the first <img> element in the article element
    without the sizes appended to the end (320w, 640w, etc.).

    This function is more efficient than the previous one because it only finds
    the first <img> element and doesn't use find_elements.
    """
    image_element = article.find_element(By.TAG_NAME, 'img')
    
    image_url = image_element.get_attribute('srcset')
    # remove the '320w', '640w', '960w', '1200w' from the url
    image_url: str = re.sub(r'[a-z0-9]*w\.', '', image_url)
    # remove leading and trailing spaces
    image_url = image_url.strip()
    
    return image_url

def get_title(article: WebElement) -> str:
    return article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a').text

def get_article_url(article: WebElement) -> str:
    return article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a').get_attribute('href')

def get_highlight(article: WebElement) -> str:
    return article.find_element(By.CLASS_NAME, 'card-text').text

def get_time_publish(article: WebElement) -> str:
    return article.find_element(By.TAG_NAME, 'time').text

def get_news(number_of_pages_to_scrape: int, driver: webdriver.Chrome, url: str) -> list[dict]:

    news = []

    for category in AlainNewsCategory:

        initialize_driver(url, category)

        pages_to_scrape = number_of_pages_to_scrape

        while pages_to_scrape > 0:
            
            pages_to_scrape = pages_to_scrape - 1

            articles = get_all_articles_on_page_by_category(driver)

            for article in articles:
                news.append({
                    "image_url": get_image_url(article),
                    "title": get_title(article),
                    "article_url": get_article_url(article),
                    "highlight": get_highlight(article),
                    "time_publish": get_time_publish(article),
                    "category": category.value
                })

            next = get_next_page_element(driver)
            
            if next.text == AlainNewsButton.NEXT_PAGE.value and pages_to_scrape > 0:
                driver.execute_script("arguments[0].click();", next)
            else:
                break

    return news

news = get_news(1, driver, url)

for n in news:
    driver.get(n.get('article_url'))
    detail_content = driver.find_element(By.ID, 'content-details').text
    publisher_name = driver.find_element(By.CLASS_NAME, 'card-author').text
    date_published = driver.find_element(By.CLASS_NAME, 'tags').find_element(By.TAG_NAME, 'time').text
    n["date_published"] = date_published
    n["publisher_name"] = publisher_name
    n["detail_content"] = detail_content
    

driver.quit()


