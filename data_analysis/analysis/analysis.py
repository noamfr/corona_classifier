from numpy import ndarray
from typing import Dict

from .age_analysis.age_analysis import Age_Analysis
from .binary_fields_analysis.binary_fields_analysis import Binary_Fields_Analysis
from .continuous_fields_analysis.continuous_fields_analysis import Continuous_Fields_Analysis
from analysis.continuous_data_fields_QA.continuous_data_fields_QA import continuous_data_fields_QA
from data.data import Data
from .missing_values_analysis.missing_values_analysis import Missing_Values_Analysis


class Analysis:
    def __init__(self, data: Data):
        self.__data = data
        self.__patients = self.__data.patients
        self.__vectors = self.__data.analysis_vectors

        self.report_tables: Dict = {}
        self.graph_vectors: Dict[str: ndarray] = {}

        self.__calc()

    def __calc(self):
        self.__missing_values_analysis()
        self.__binary_fields_analysis()
        self.__continuous_data_fields_QA()
        self.__continuous_fields_analysis()
        # self.__age_analysis()

    def __missing_values_analysis(self):
        missing_values_analysis = Missing_Values_Analysis(patients=self.__patients)
        self.report_tables = {**self.report_tables, **missing_values_analysis.get_report_tables}
        self.graph_vectors = {**self.graph_vectors, **missing_values_analysis.get_graph_vectors}

    def __binary_fields_analysis(self):
        binary_fields_analysis = Binary_Fields_Analysis(patients=self.__patients, vectors=self.__vectors)
        self.report_tables = {**self.report_tables, **binary_fields_analysis.get_report_tables}

    def __continuous_data_fields_QA(self):
        continuous_data_fields_qa = continuous_data_fields_QA(patients=self.__patients)
        self.report_tables = {**self.report_tables, **continuous_data_fields_qa.report_tables}

    def __continuous_fields_analysis(self):
        continuous_fields_analysis = Continuous_Fields_Analysis(patients=self.__patients, vectors=self.__vectors)
        self.report_tables = {**self.report_tables, **continuous_fields_analysis.get_report_tables}
        self.graph_vectors = {**self.graph_vectors, **continuous_fields_analysis.get_graph_vectors}

    def __age_analysis(self):
        age_analysis = Age_Analysis(patients=self.__patients, publish_results=True)
        age_analysis.run_analysis()
