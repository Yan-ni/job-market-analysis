from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import logging
import re
import json


def wait_for_all_requests_to_complete(driver: WebDriver) -> bool:
    logs = driver.get_log("performance")  # Get network logs
    pending_requests = 0

    for log in logs:
        log_entry = json.loads(log["message"])["message"]

        if log_entry["method"] == "Network.requestWillBeSent":
            pending_requests += 1
        elif log_entry["method"] == "Network.responseReceived":
            pending_requests -= 1

    if pending_requests <= 0:
        logging.debug("✅ All requests are complete.")
        return True

    logging.debug("❌ All requests didn't complete yet")
    return False


class Scraper:
    """A representation of the scraper that is a combination of selenium and beautiful soup."""

    @staticmethod
    def get_url_soup(url: str) -> BeautifulSoup:
        """Fetch the url and return its page source soup."""
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.set_capability(
            "goog:loggingPrefs", {"performance": "ALL"}
        )  # capture network logs
        browser = Chrome(
            options=chrome_options
        )  # Path to chromium argument is optional, if not specified will search path.
        browser.get(url)
        wait = WebDriverWait(browser, timeout=60, poll_frequency=2)
        wait.until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
            and wait_for_all_requests_to_complete(driver)
        )

        return BeautifulSoup(browser.page_source, "html.parser")

    @staticmethod
    def get_soup_text(soup: BeautifulSoup) -> str:
        """Get text from a multi line text.
        This method prevents having randomly broken words or inconsistent returns.
        """
        text_list = list()
        soup_elements = soup.find_all(["p", "li", "h4"])

        if len(soup_elements) == 0:
            return None

        for soup_element in soup_elements:
            if (
                soup_element.p
            ):  # prevent having duplicate lines in case of: <li><p>...</p></li>
                continue

            for br in soup_element.find_all("br"):
                br.replace_with("\n")

            text_list.append(soup_element.get_text(""))

        text = "\n".join(text_list)
        text = re.sub(
            re.compile(r"\n{3,}"), "\n\n", text
        )  # prevent having more than 2 line returns
        text = re.sub(
            re.compile(r":\n{2,}"), ":\n", text
        )  # prevent having an empty line after a sentence ending with ":"
        text = re.sub(
            re.compile(r"([^\n])(\n.*:)"), r"\1\n\2", text
        )  # prevent having empty lines before sentence ending with ":"

        return text
