import pandas as pd
from configuration.config import Config
from data_layer.raw_data_api import Raw_Data_Api
from pre_analysis.pre_analysis_api import Pre_Analysis_Api


class Pipeline:
    def __init__(self):
        self.raw_df = None

    def get_data(self):
        raw_data_api = Raw_Data_Api()
        self.raw_df = raw_data_api.get_raw_data()

    def preliminary_analysis(self):
        pre_analysis_api = Pre_Analysis_Api(raw_df=self.raw_df)
        pre_analysis_api.run_pre_analysis()

    def prep_data(self):
        print('data is prepped')

    def basic_analysis(self):
        pass

    def run_classification(self):
        pass
