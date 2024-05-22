from enum import Enum
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException

class AlainNewsCategory(Enum):
    POLITICS = 'politics'
    SOCIAL = 'social'
    ECONOMY = 'economy'
    VARIETIES = 'varities'
    SPORT = 'sports'

class AlainNewsButton(Enum):
    LOADING = "ተጨማሪ ጫን"
    NEXT_PAGE = 'next page'

class AlainNewsScraper:
    def __init__(
        self, 
        url: str, 
        headless: bool = True, 
        number_of_pages_to_scrape: int = 1
    ) -> None:
        """
        Initialize the AlainNewsScraper object

        Args:
            url (str): The URL of the Alain news website
            headless (bool, optional): Whether to run the web driver in headless mode. Defaults to True.
            number_of_pages_to_scrape (int, optional): The number of pages of articles to scrape. Defaults to 1.
        """
        # Create a new instance of the Chrome web driver
        # We use headless mode to avoid seeing the browser window pop up
        # in the background while the script is running
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            options=options, 
            service=Service(ChromeDriverManager().install())
        )
        # Store the URL of the website we're scraping and the number of
        # pages of articles to scrape
        self.url = url
        self.number_of_pages_to_scrape = number_of_pages_to_scrape

    def scroll_to_bottom(self) -> None:
        """
        Scrolls the web page to the bottom using JavaScript.

        This function executes a JavaScript command to scroll the web page to the bottom.
        It uses the `execute_script` method of the `driver` object to execute the command.
        The command is `"window.scrollTo(0, document.body.scrollHeight);"`, which scrolls the page
        to the bottom by setting the scroll position to the maximum height of the document body.

        Raises:
            WebDriverException: If an error occurs while scrolling to the bottom of the page.

        Returns:
            None
        """
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except WebDriverException as e:
            print("WebDriverException error occurred while scrolling to the bottom of the page:", e)
            raise

    def initialize_driver(self, category: AlainNewsCategory) -> None:
        """
        Initializes the web driver and navigates to the specified category page.

        Args:
            category (AlainNewsCategory): The category to navigate to.

        Raises:
            WebDriverException: If an error occurs while navigating to the category page.

        Returns:
            None
        """
        category_page_url = f"{self.url}/section/{category.value}/"
        
        try:
            self.driver.get(category_page_url)
        except WebDriverException as e:
            print("WebDriverException error occurred while navigating to the category page:", e)
            raise

    def get_all_articles_on_page_by_category(self) -> list[WebElement]:
        """
        Retrieves all the articles on the current page for a given category.

        This function performs the following steps:

            1. Scrolls to the bottom of the page to load more articles, if available.
            2. Retrieves the next page element and checks if it is still loading.
            3. If it is, waits until the loading is complete and retrieves the articles element.

        Returns:
            list[WebElement]: A list of WebElement objects representing the articles on the current page for the given category.

        Raises:
            WebDriverException: If an error occurs while retrieving the article elements.
        """

        # Scroll to the bottom of the page to load more articles
        try:
            self.scroll_to_bottom()
        except WebDriverException as e:
            print("WebDriverException error occurred while scrolling to the bottom of the page:", e)
            raise

        # Retrieve the next page element and check if it is still loading
        next_page = self.get_next_page_element()
        while next_page.text == AlainNewsButton.LOADING.value:
            try:
                # If it is, wait until the loading is complete and retrieve the articles element
                next_page = self.get_next_page_element()
            except WebDriverException as e:
                print("WebDriverException error occurred while waiting for the next page element to load:", e)
                raise

        # Return the articles element
        try:
            return self.get_articles_element()
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the article elements:", e)
            raise


    def get_articles_element(self) -> list[WebElement]:
        try:
            row_element = self.driver.find_element(By.XPATH, '//div[@class="row loadmore"]')
            articles = row_element.find_elements(By.TAG_NAME, 'article')
            if not articles:
                print("No articles found on the page.")
            return articles
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the article elements:", e)
            return []

    def get_next_page_element(self) -> WebElement:
        try:
            footer_element = self.driver.find_elements(By.TAG_NAME, 'footer')[0]
            return footer_element.find_element(By.TAG_NAME, 'a')
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the next page element:", e)
            raise

    def get_image_url(self, article: WebElement) -> str:
        try:
            image_element = article.find_element(By.TAG_NAME, 'img')
            image_url = image_element.get_attribute('srcset')
            image_url = re.sub(r'\s\d+w', '', image_url).split(',')[0]
            return image_url.strip()
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the image url of the article:", e)
            return ""

    def get_title(self, article: WebElement) -> str:
        try:
            title_element = article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a')
            return title_element.text
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the title of the article:", e)
            return ""

    def get_article_url(self, article: WebElement) -> str:
        try:
            title_element = article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a')
            return title_element.get_attribute('href')
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the article url of the article:", e)
            return ""

    def get_highlight(self, article: WebElement) -> str:
        try:
            highlight_element = article.find_element(By.CLASS_NAME, 'card-text')
            return highlight_element.text
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the highlight of the article:", e)
            return ""

    def get_time_publish(self, article: WebElement) -> str:
        try:
            time_element = article.find_element(By.TAG_NAME, 'time')
            return time_element.text
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the time publish of the article:", e)
            return ""

    def get_news(self) -> list[dict]:
        news = []
        for category in AlainNewsCategory:
            self.initialize_driver(category)
            pages_to_scrape = self.number_of_pages_to_scrape
            while pages_to_scrape > 0:
                pages_to_scrape -= 1
                articles = self.get_all_articles_on_page_by_category()
                if not articles:
                    print(f"No articles found on page {pages_to_scrape + 1} of category {category.value}")
                else:
                    for article in articles:
                        try:
                            news.append({
                                "image_url": self.get_image_url(article),
                                "title": self.get_title(article),
                                "article_url": self.get_article_url(article),
                                "highlight": self.get_highlight(article),
                                "time_publish": self.get_time_publish(article),
                                "category": category.value
                            })
                        except (WebDriverException, AttributeError, Exception) as e:
                            print(f"An error occurred while scraping article on page {pages_to_scrape + 1} of category {category.value}:", e)
                next = self.get_next_page_element()
                if next.text == AlainNewsButton.NEXT_PAGE.value and pages_to_scrape > 0:
                    self.driver.execute_script("arguments[0].click();", next)
                else:
                    break
        return news

    def get_full_news(self) -> list[dict]:
        news = self.get_news()
        for n in news:
            print("The article on page of category {} is: {}".format(n.get('category'), n.get('article_url')))
            try:
                self.driver.get(n.get('article_url'))
                detail_content = self.driver.find_element(By.ID, 'content-details').text
                publisher_name = self.driver.find_element(By.CLASS_NAME, 'card-author').text
                date_published = self.driver.find_element(By.CLASS_NAME, 'tags').find_element(By.TAG_NAME, 'time').text
                n["date_published"] = date_published
                n["publisher_name"] = publisher_name
                n["detail_content"] = detail_content
            except (WebDriverException, AttributeError, Exception) as e:
                print(f"An error occurred while scraping content page of category {n.get('category')} :: {e}")
        return news

    def quit_driver(self):
        self.driver.quit()