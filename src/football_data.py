import logging
import os
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)


class FootballData:

    def __init__(self):
        pass

    def read_data(self):
        df_bra = pd.read_csv(f"{Path(os.getcwd())}/resources/BRA.csv", sep=",")
        df_eng = pd.read_csv(f"{Path(os.getcwd())}/resources/E0.csv", sep=",")
        df_spa = pd.read_csv(f"{Path(os.getcwd())}/resources/SP1.csv", sep=",")
        return df_bra, df_eng, df_spa

    def rename_columns(self, df):
        columns = {'HG': 'Home_Goals',
                   'AG': 'Away_Goals', 'HR': 'Home_Rewards',
                   'Res': 'Result'}
        df.rename(columns=columns, inplace=True)

    def get_football_data(self):
        df_bra, df_eng, df_spa = self.read_data()
        # self.rename_columns(df_bra)
        log.info(df_bra.head())
        log.info(df_eng.head())
        log.info(df_spa.head())
