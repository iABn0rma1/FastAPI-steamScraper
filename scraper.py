import re
import time
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

class SteamStoreScraper:
    """
    A class to scrape game data from the Steam store.

    Example Usage:
    ```python
    steam = SteamStoreScraper()
    result = steam.scrape_games(n_games=5, tags=["Discounts", "F2P"])
    ```
    """

    def __init__(self, region="IN"):
        self.base_url = f"https://store.steampowered.com/search/?supportedlang=english&cc={region}&category1=998%2C21&"
        self.cols = [
            "Name",
            "image_url",
            "href",
            "Date",
            "Platforms",
            "Original_Price",
            "discountPrcnt",
            "discount_price",
            "Reviews",
            "Reviews_Prcnt",
            "Filter",
        ]

    def _get_total_pages(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            doc = BeautifulSoup(response.content, "html.parser")
            pagination_div = doc.find("div", {"class": "search_pagination_right"})
            if pagination_div:
                total_pages = int(pagination_div.find_all("a")[-2].text)
                return total_pages
            return 1
        except (requests.RequestException, ValueError, IndexError):
            return 1

    def _extract_game_info(self, game):
        try:
            name = game.find("span", {"class": "title"}).text
            published_date = game.find(
                "div", {"class": "col search_released responsive_secondrow"}
            ).text.strip() or None

            image_div = game.find('div', class_='search_capsule')
            image_url = image_div.find('img')['src'] if image_div else None

            href = game.get('href')

            div_element = game.find("div", class_="col search_name ellipsis")
            platform_images = div_element.find_all("span", class_="platform_img")
            platforms = [
                img.get("class")[1] if len(img.get("class")) > 1 else None
                for img in platform_images
            ]

            original_price_elem = game.find("div", {"class": "discount_original_price"})
            original_price = original_price_elem.text.strip() if original_price_elem else None

            discount_pct_elem = game.find("div", {"class": "discount_pct"})
            discount_pct = discount_pct_elem.text.strip() if discount_pct_elem else None

            discount_price_elem = game.find("div", {"class": "discount_final_price"})
            discount_price = discount_price_elem.text.strip() if discount_price_elem else None

            review_summary = game.find("span", {"class": "search_review_summary"})
            reviews_html = review_summary["data-tooltip-html"] if review_summary else None
            pattern = r"(.+)<br>(\d+%)\s+of\s+the\s+([\d,]+)\s+user reviews.*"
            match = re.match(pattern, reviews_html)
            sentiment = match.group(1) if match else None
            percentage = match.group(2) if match else None

            # reviews = f"{sentiment.strip()} - {percentage.strip()}" if sentiment and percentage else None

        except Exception as e:
            logging.error(f"Error extracting game info: {e}")
            return None

        return (
            name,
            image_url,
            href,
            published_date,
            platforms,
            original_price,
            discount_pct,
            discount_price,
            sentiment,
            percentage,
        )

    def _scrape_page(self, url, filter, n0Games):
        """
        Scrapes game data for a given URL and filter.

        Args:
            url (str): The URL to scrape.
            filter (str): The filter for the game data.

        Returns:
            list: List of game data for the filter.
        """
        all_game_info = []

        try:
            response = requests.get(url)
            response.raise_for_status()
            doc = BeautifulSoup(response.content, "html.parser")
            games = doc.find_all(
                "a", {"class": "search_result_row ds_collapse_flag"}
            )

            for game in games:
                game_info = self._extract_game_info(game)
                print(f"game_info: {game_info}")
                if game_info is not None:
                    all_game_info.append([*game_info, filter])
                else:
                    print("game_info is None")


                if len(all_game_info) >= n0Games:
                    break
        except requests.RequestException as e:
            logging.error(f"Error fetching page data: {e}")
        
        return all_game_info

    def ScrapeGames(self, n0Games=100, offset=0):
        all_data = []
        filters = "specials=1"
        
        while len(all_data) < n0Games:
            url = f"{self.base_url}{filters}&start={offset}"
            filter_data = self._scrape_page(url, filters, n0Games - len(all_data))
            all_data.extend(filter_data)
            
            offset += len(filter_data)
            if not filter_data:
                break
            
            time.sleep(1)  # delay between requests

        data = {col: [] for col in self.cols}
        for row in all_data:
            for col, value in zip(self.cols, row):
                data[col].append(value)

        return self.__to_readable_format(data)

    def __to_readable_format(self, data):
        readable_data = []
        for i in range(len(data["Name"])):
            game_data = {col: data[col][i] for col in self.cols}
            del game_data["Filter"]
            readable_data.append(game_data)
        return readable_data
