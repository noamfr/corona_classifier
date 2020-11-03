from numpy import ndarray
from typing import Dict

from .age_analysis.age_analysis import Age_Analysis
from .binary_fields_analysis.binary_fields_analysis import Binary_Fields_Analysis
from .continuous_fields_analysis.continuous_fields_analysis import Continuous_Fields_Analysis
from data.data import Data
from .missing_values_analysis.missing_values_analysis import Missing_Values_Analysis


class Analysis:
    def __init__(self, data: Data):
        self.__patients = data.get_patients
        self.__vectors = data.get_vectors
        self.__report_tables: Dict = {}
        self.__output_graph_vectors: Dict[str: ndarray] = {}

        self.__calc()

    def __calc(self):
        self.__missing_values_analysis()
        self.__binary_fields_analysis()
        self.__continuous_fields_analysis()
        # self.__age_analysis()

    def __missing_values_analysis(self):
        missing_values_analysis = Missing_Values_Analysis(patients=self.__patients)
        self.__report_tables = {**self.__report_tables, **missing_values_analysis.get_report_tables}
        self.__output_graph_vectors = {**self.__output_graph_vectors, **missing_values_analysis.get_graph_vectors}

    def __binary_fields_analysis(self):
        binary_fields_analysis = Binary_Fields_Analysis(patients=self.__patients, vectors=self.__vectors)
        self.__report_tables = {**self.__report_tables, **binary_fields_analysis.get_report_tables}

    def __continuous_fields_analysis(self):
        continuous_fields_analysis = Continuous_Fields_Analysis(patients=self.__patients, vectors=self.__vectors)
        self.__report_tables = {**self.__report_tables, **continuous_fields_analysis.get_report_tables}
        self.__output_graph_vectors = {**self.__output_graph_vectors, **continuous_fields_analysis.get_graph_vectors}

    def __age_analysis(self):
        age_analysis = Age_Analysis(patients=self.__patients, publish_results=True)
        age_analysis.run_analysis()

    @property
    def get_report_tables(self):
        return self.__report_tables

    @property
    def get_graph_vectors(self):
        return self.__output_graph_vectors
