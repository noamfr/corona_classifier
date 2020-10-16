from collections import defaultdict


from .age_analysis.age_analysis import Age_Analysis
from .binary_fields_analysis.binary_fields_analysis import Binary_Fields_Analysis
from .continuous_fields_analysis.continuous_fields_analysis import Continuous_Fields_Analysis
from data.data import Data, Data_Fields


class Analysis:
    def __init__(self, data: Data):
        self.patients = data.patients

    def calc(self):
        self.__binary_fields_analysis()
        self.__continuous_fields_analysis()
        self.__age_analysis()

    def __get_binary_unique_values(self):
        binary_data_fields = Data_Fields.get_binary_vars()
        binary_vars_unique = defaultdict(set)
        for patient in self.patients:
            for field in binary_data_fields:
                value = getattr(patient, field)
                binary_vars_unique[field].add(value)

        return binary_vars_unique

    def __binary_fields_analysis(self):
        binary_fields_analysis = Binary_Fields_Analysis(patients=self.patients, publish_results=True)
        binary_fields_analysis.run_analysis()

    def __continuous_fields_analysis(self):
        continuous_fields_analysis = Continuous_Fields_Analysis(patients=self.patients, publish_results=True)
        continuous_fields_analysis.run_analysis()

    def __continuous_fields_quality(self):
        pass

    def __age_analysis(self):
        age_analysis = Age_Analysis(patients=self.patients, publish_results=True)
        age_analysis.run_analysis()
