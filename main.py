import logging

from playwright.sync_api import sync_playwright

from src.extractors.extractor_football_data import ExtractorFootballData
from src.extractors.extractor_xscores import ScrapXScores
from src.football_data import FootballData

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    markets = {
        # MAIN LEAGUES
        # "England": "englandm.php",
        # "France": "francem.php",
        # "Italy": "italym.php",
        # "Spain": "spainm.php",
        "Germany": "germanym.php",
        # EXTRA LEAGUES
        "Brazil": "brazil.php",
        "Japan": "japan.php",
    }

    # client = ExtractorFootballData("https://www.football-data.co.uk", markets)
    # client.extract()
    # log.info(client.dict_data_updated)
    # log.info(client.dict_items)

    # football_data = FootballData()
    # football_data.get_football_data()

    with sync_playwright() as playwright:
        scraper = ScrapXScores(playwright, False)
        scraper.extract_league_standings("spain")
