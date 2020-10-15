from .binary_fields_analysis.binary_fields_analysis import Binary_Fields_Analysis
from .age_analysis.age_analysis import Age_Analysis
from .continuous_fields_analysis.continuous_fields_analysis import Continuous_Fields_Analysis


class Exploratory_Analysis:
    def __init__(self, patients):
        self.patients = patients

    def calc(self):
        self.__binary_fields_analysis()
        self.__continuous_fields_analysis()
        self.__age_analysis()

    def __binary_fields_analysis(self):
        binary_fields_analysis = Binary_Fields_Analysis(patients=self.patients, publish_results=True)
        binary_fields_analysis.run_analysis()

    def __continuous_fields_analysis(self):
        continuous_fields_analysis = Continuous_Fields_Analysis(patients=self.patients, publish_results=True)
        continuous_fields_analysis.run_analysis()

    def __age_analysis(self):
        age_analysis = Age_Analysis(patients=self.patients, publish_results=True)
        age_analysis.run_analysis()
