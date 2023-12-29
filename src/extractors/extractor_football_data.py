import logging
import os
import re
from collections import namedtuple
from pathlib import Path

import requests
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

data_item = namedtuple('data_item', ["league", "url", "file_name", "text"])


class ExtractorFootballData:

    def __init__(self, endpoint, markets: dict):
        self.session = requests.Session()
        self.endpoint = endpoint
        self.path_resources = Path(os.getcwd()) / 'resources'
        self.path_resources.mkdir(parents=True, exist_ok=True)

        self.dict_items = dict()
        self.dict_data_updated = dict()

        # Add initial links
        self.link_dict = dict()
        self.link_dict = {k: f"{endpoint}/{v}" for k, v in markets.items()}

    def extract_patterns(self, html_text):
        data_file = ""
        last_updated = ""

        pattern = r'(?<=Data Files: )[ A-Za-z0-9]+'
        # <b>Data Files: Brazil</b>
        re_data_files = re.findall(pattern, html_text)
        if re_data_files and len(re_data_files) > 0:
            data_file = re_data_files[0].strip()

        pattern = r'(?<=Last updated: )[ \t/0-9\\]+'
        # <i>Last updated: 	08/12/23</i>
        re_last_updated = re.findall(pattern, html_text)
        if re_last_updated and len(re_last_updated) > 0:
            last_updated = re_last_updated[0].strip()

        return data_file, last_updated

    def extract(self):
        for league, url in self.link_dict.items():
            log.info(f"Extracting data from {league} - {url}")
            self.__fetch_links(league, url)

    def __fetch_links(self, league, url):
        soup = self.__get_page_soup(url)
        self.__collect_page_data(soup, league, url)

    def __get_page_soup(self, url):
        response = self.session.get(url)
        root_html = response.text
        soup = BeautifulSoup(root_html, 'html.parser')
        return soup

    def __collect_page_data(self, soup, league, url):
        data_file, last_updated = self.extract_patterns(soup.text)
        self.dict_data_updated[data_file] = last_updated

        all_links = soup.find_all('a')

        for link in all_links:
            href = link.get('href')

            if self.__is_csv_file(href):  # link is a file like: .csv, .zip, .json
                item = self.__get_data_item(link, league, url)
                self.__download_item(item)

                if data_file in self.dict_items:
                    self.dict_items[data_file].add(item)
                else:
                    self.dict_items[data_file] = set()
                    self.dict_items[data_file].add(item)
                log.info(f"added file link {item.url}")

    def __is_csv_file(self, href):
        path_href = href.split('.')
        if len(path_href) > 1 and len(path_href[-1]) <= 4 and path_href[-1] == "csv":
            return True
        return False

    def __get_data_item(self, link, league, url):
        href = link.get('href')
        file_name = self.__format_href(href)
        text = link.text
        dlink = f"{self.endpoint}/{href}"
        item = data_item(league, dlink, file_name, text)
        return item

    def __download_item(self, item):
        dir_path = Path(f"{self.path_resources}/{item.league}")
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = f"{dir_path}/{item.file_name}"

        response = self.session.get(item.url, timeout=30)
        response.raise_for_status()

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())

    def __format_href(self, href):
        return "_".join(href.split("/"))
