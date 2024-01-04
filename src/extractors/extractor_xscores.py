import pandas as pd

from playwright.sync_api import Playwright


class ScrapXScores:

    def __init__(self, playwright: Playwright, headless: bool = False):
        self.playwright = playwright
        self.headless = headless

        self.browser = playwright.chromium.launch(headless=self.headless)
        self.context1 = self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")

    def extract_league_standings(self, league_id):
        # url = "https://www.xscores.com/soccer/spain/primera-division/standings"
        url = "https://www.xscores.com/soccer/england/premier-league/standings"

        page = self.context1.new_page()
        page.set_default_timeout(25000)
        page.goto(url)
        page.wait_for_load_state()

        df_teams = pd.DataFrame()

        stream_teamns = page.locator("//div[contains(@class,'team_name')]")
        column = [team.inner_text() for team in stream_teamns.element_handles()][0]
        rows = [team.inner_text() for team in stream_teamns.element_handles()][1:]
        df_teams.insert(0, "R", [idx for idx, team in enumerate(stream_teamns.element_handles())][1:])
        df_teams = df_teams.set_index('R')
        df_teams.insert(0, column, rows)

        stream_teamns_numbers = page.locator("//div[contains(@class, 'scroll_column')]/div[contains(@class,'team_stats_wrapper')]")

        for idx, row in enumerate(stream_teamns_numbers.element_handles()):
            stream_cols_numbers = row.query_selector_all(".number_cell")
            stream_cols_form = row.query_selector_all(".form_div")

            if idx == 0:
                cols_number = []
                cols_form = []

                for col in stream_cols_numbers:
                    number_text = col.inner_text()
                    df_teams[number_text] = ""
                    cols_number.append(number_text)

                for col in stream_cols_form:
                    form_text = col.inner_text()
                    df_teams[form_text] = ""
                    cols_form.append(form_text)

            else:
                for idx_col, col in enumerate(stream_cols_numbers):
                    number_text = col.inner_text()
                    df_teams.at[idx, cols_number[idx_col]] = number_text

                for idx_col, col in enumerate(stream_cols_form):
                    stream_cols_form_elmt = col.query_selector_all(".form_elmt")
                    form_text = ",".join([form_elmt.inner_text() for form_elmt in stream_cols_form_elmt])
                    df_teams.at[idx, cols_form[idx_col]] = form_text

        print(df_teams)