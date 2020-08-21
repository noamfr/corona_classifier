from get_data.data_reader import Data_Reader
from missing_values.missing_values import Missing_Values
from data.prep_data import Prep_Data
from basic_analysis.basic_analysis import Basic_Analysis


class Pipeline:
    def __init__(self):
        self.patients = []
        self.fields_not_in_analysis = []

    def get_data(self):
        data_reader = Data_Reader()
        self.patients = data_reader.get_patients()

    def treat_missing_values(self):
        missing_values_remover = Missing_Values(patients=self.patients)
        missing_values_remover.remove_data_fields_with_to_much_missing_data()

    def prep_data(self):
        prep_data = Prep_Data(patients=self.patients)
        prep_data.prep_data()
        self.patients = prep_data.patients

    def basic_analysis(self):
        basic_analysis = Basic_Analysis(patients=self.patients)
        basic_analysis.calc()

    def run_classification(self):
        pass
