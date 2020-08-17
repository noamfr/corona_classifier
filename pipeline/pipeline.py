from get_data_layer.data_reader import Data_Reader
from pre_analysis.data_api import Data_Api
from data_layer.prep_data_api import Prep_Data_Api


class Pipeline:
    def __init__(self):
        self.patients = []

    def get_data(self):
        data_reader = Data_Reader()
        self.patients = data_reader.read_data()

    def prep_data(self):
        data_api = Data_Api(patients=self.patients)
        data_api.run_missing_value_analysis()

    def prep_data_old(self):
        prep_data_api = Prep_Data_Api(patients=self.patients)
        # prep_data_api.prep_data()
        # self.prep_df = prep_data_api.df

    def basic_analysis(self):
        pass

    def run_classification(self):
        pass
