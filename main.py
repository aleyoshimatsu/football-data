import logging

from src.extractors.extractor_football_data import ExtractorFootballData
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

    client = ExtractorFootballData("https://www.football-data.co.uk", markets)
    client.extract()

    # football_data = FootballData()
    # football_data.get_football_data()
