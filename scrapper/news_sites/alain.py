from enum import Enum
import re
from selenium.common.exceptions import WebDriverException
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

def scroll_to_bottom(driver: webdriver.Chrome) -> None:
    """
    Scrolls the page to the bottom using the execute_script method.
    
    This function checks for null pointer references, unhandled exceptions, and more.
    """
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except WebDriverException:
        print("WebDriverException error occurred while scrolling to the bottom of the page:")
        raise
    except AttributeError as e:
        # Handle AttributeError
        print("AttributeError error occurred while scrolling to the bottom of the page:")
        print(e)
        raise
    except Exception as e:
        # Handle any other exceptions
        print("An unexpected error occurred while scrolling to the bottom of the page:")
        print(e)
        raise

def initialize_driver(base_url: str, category: AlainNewsCategory) -> None:
    """
    Initializes the webdriver with the url of the category page of Alain News
    """
    category_page_url = f"{base_url}/section/{category.value}/"
    
    try:
        driver.get(category_page_url)
    except WebDriverException:
        print("WebDriverException error occurred while navigating to the category page:")
        raise
    except Exception as e:
        # Handle any other exceptions
        print("An unexpected error occurred while navigating to the category page:")
        print(e)
        raise

def get_all_articles_on_page_by_category(driver: webdriver.Chrome) -> list[WebElement]:
    """
    Return a list of all article elements on the page.

    This function checks for null pointer references, unhandled exceptions, and
    more.
    """
    try:
        # Scroll down
        scroll_to_bottom(driver)

        # Get the next page button
        next_page = get_next_page_element(driver)

        # Check until the next page button is available which changes from
        # "ተጨማሪ ጫን" to "next page"
        while next_page.text == AlainNewsButton.LOADING.value:
            next_page = get_next_page_element(driver)

        # Now we have got all the pages loaded with all possible articles    
        articles = get_articles_element(driver)

        return articles
    except WebDriverException as e:
        # Handle WebDriverException
        print("WebDriverException error occurred while retrieving the article elements:")
        print(e)
        raise
    except AttributeError as e:
        # Handle AttributeError
        print("AttributeError error occurred while retrieving the article elements:")
        print(e)
        raise
    except Exception as e:
        # Handle any other exceptions
        print("An unexpected error occurred while retrieving the article elements:")
        print(e)
        raise

def get_articles_element(driver: webdriver.Chrome) -> list[WebElement]:
    """
    Return a list of all article elements on the page.

    This function checks for null pointer references and unhandled exceptions.
    """
    try:
        # Find the row element with the loadmore class
        row_element = driver.find_element(By.XPATH, '//div[@class="row loadmore"]')
        # Find all article elements inside the row element
        articles = row_element.find_elements(By.TAG_NAME, 'article')
        # If no articles are found, print an error message
        if len(articles) == 0:
            print("No articles found on the page.")
        # Return the list of articles
        return articles
    except WebDriverException:
        print("WebDriverException error occurred while retrieving the article elements:")
        # The row element does not exist, so return an empty list
        return []
    except Exception as e:
        # Handle any other exceptions
        print("An unexpected error occurred while retrieving the article elements:")
        print(e)
        return []

def get_next_page_element(driver: webdriver.Chrome) -> WebElement:
    """
    Return the next page button element.

    This function checks for null pointer references and unhandled exceptions.
    """
    try:
        footer_element = driver.find_elements(By.TAG_NAME, 'footer')[0]
        next_page_element = footer_element.find_element(By.TAG_NAME, 'a')
        return next_page_element
    except WebDriverException:
        print("WebDriverException error occurred while retrieving the next page element:")
        raise
    except Exception as e:
        # Handle any other exceptions
        print("An unexpected error occurred while retrieving the next page element:")
        print(e)
        raise

def get_image_url(article: WebElement) -> str:
    """Return the srcset attribute of the first <img> element in the article element
    without the sizes appended to the end (320w, 640w, etc.).

    This function is more efficient than the previous one because it only finds
    the first <img> element and doesn't use find_elements.
    """
    try:
        image_element = article.find_element(By.TAG_NAME, 'img')
        
        image_url = image_element.get_attribute('srcset')
        # remove the '320w', '640w', '960w', '1200w' from the url
        image_url: str = re.sub(r'[a-z0-9]*w\.', '', image_url)
        # remove leading and trailing spaces
        image_url = image_url.strip()
        
        return image_url
    except WebDriverException:
        print("WebDriverException error occurred while retrieving the image url of the article:")
        # The image element does not exist, so return an empty string
        return ""
    except AttributeError as e:
        # Handle AttributeError exception
        print("AttributeError error occurred while retrieving the image url of the article:")
        print(e)
        return ""
    except Exception as e:
        # Handle any other exceptions
        print("An unexpected error occurred while retrieving the image url of the article:")
        print(e)
        return ""

def get_title(article: WebElement) -> str:
    """
    Return the title of the article.

    This function checks for null pointer references and unhandled exceptions.
    """
    try:
        title_element = article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a')
        return title_element.text
    except WebDriverException:
        print("WebDriverException error occurred while retrieving the title of the article:")
        # The title element does not exist, so return an empty string
        return ""
    except Exception as e:
        # Handle any other exceptions
        print("An unexpected error occurred while retrieving the title of the article:")
        print(e)
        return ""

def get_article_url(article: WebElement) -> str:
    """
    Return the href attribute of the first <a> element in the article element.

    This function checks for null pointer references and unhandled exceptions.
    """
    try:
        title_element = article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a')
        return title_element.get_attribute('href')
    except WebDriverException:
        print("WebDriverException error occurred while retrieving the article url of the article:")
        # The title element does not exist, so return an empty string
        return ""
    except Exception as e:
        # Handle any other exceptions
        print("An unexpected error occurred while retrieving the article url of the article:")
        print(e)
        return ""

def get_highlight(article: WebElement) -> str:
    """
    Return the text content of the first <div class="card-text"> element in the article element.

    This function checks for null pointer references and unhandled exceptions.
    """
    try:
        highlight_element = article.find_element(By.CLASS_NAME, 'card-text')
        return highlight_element.text
    except WebDriverException:
        print("WebDriverException error occurred while retrieving the highlight of the article:")
        # The highlight element does not exist, so return an empty string
        return ""
    except Exception as e:
        # Handle any other exceptions
        print("An unexpected error occurred while retrieving the highlight of the article:")
        print(e)
        return ""


def get_time_publish(article: WebElement) -> str:
    """
    Return the text content of the first <time> element in the article element.

    This function checks for null pointer references and unhandled exceptions.
    """
    try:
        time_element = article.find_element(By.TAG_NAME, 'time')
        return time_element.text
    except WebDriverException:
        print("WebDriverException error occurred while retrieving the time publish of the article:")
        # The time element does not exist, so return an empty string
        return ""
    except Exception as e:
        # Handle any other exceptions
        print("An unexpected error occurred while retrieving the time publish of the article:")
        print(e)
        return ""

def get_news(number_of_pages_to_scrape: int, driver: webdriver.Chrome, url: str) -> list[dict]:
    
    news = []
    
    for category in AlainNewsCategory:
        
        initialize_driver(url, category)
        
        pages_to_scrape = number_of_pages_to_scrape
        
        while pages_to_scrape > 0:
            
            pages_to_scrape = pages_to_scrape - 1
            
            articles = get_all_articles_on_page_by_category(driver)
            
            if len(articles) == 0:
                print(f"No articles found on page {pages_to_scrape + 1} of category {category.value}")
            else:
                for article in articles:
                    try:
                        news.append({
                            "image_url": get_image_url(article),
                            "title": get_title(article),
                            "article_url": get_article_url(article),
                            "highlight": get_highlight(article),
                            "time_publish": get_time_publish(article),
                            "category": category.value
                        })
                    except (WebDriverException, AttributeError, Exception) as e:
                        print(f"An error occurred while scraping article on page {pages_to_scrape + 1} of category {category.value}:")
                        print(e)
                        
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


