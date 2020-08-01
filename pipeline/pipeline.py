import pandas as pd
from configuration.config import Config
from data_layer.raw_data_api import Raw_Data_Api


class Pipeline:
    def __init__(self):
        self.raw_data = pd.DataFrame

    def get_data(self):
        raw_data_api = Raw_Data_Api()
        self.raw_data = raw_data_api.get_raw_data()

    def prep_data(self):
        pass

    def basic_analysis(self):
        pass

    def run_classification(self):
        pass
