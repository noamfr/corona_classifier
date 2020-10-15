import os
import numpy as np
from typing import List

from data_operations.data_frame_printer import Data_Frame_Printer
from analysis_operations.descriptive_table import Descriptive_Table
from analysis_operations.graph_functions import histogram

from corona_data_analysis.config.config import Config


class Age_Analysis:
    def __init__(self, patients: List, publish_results: bool):
        self.patients = patients
        self.publish_results = publish_results
        self.local_output_path = os.path.join(Config.OUTPUT_PATH, 'age_analysis')

        self.continuous_vectors = None
        self.categorical_vectors = None
        self.age_descriptive_table = None

        self.__generate_age_vectors()

    def run_analysis(self):
        self.age_descriptive_table = self.__age_descriptive_table()
        self.__age_vector_histograms()

        if self.publish_results:
            self.__print_results()

    def __print_results(self):
        data_frame_printer = Data_Frame_Printer(path=self.local_output_path)
        data_frame_printer.print_df_from_defaultdict(self.age_descriptive_table, 'age_descriptive_table')

    def __generate_age_vectors(self):
        all_ages = np.array([patient.age for patient in self.patients])
        adult_ages = np.array([patient.age for patient in self.patients if patient.is_adult == 1])
        children_ages = np.array([patient.age for patient in self.patients if patient.is_adult == 0])

        is_adult = np.array([patient.is_adult for patient in self.patients])
        age_categorical = np.array([patient.age_category for patient in self.patients])

        continuous_vectors = {'all_ages': all_ages, 'adult_ages': adult_ages, 'children_ages': children_ages}
        categorical_vectors = {'is_adult': is_adult, 'age_categorical': age_categorical}

        self.continuous_vectors = continuous_vectors
        self.categorical_vectors = categorical_vectors

    def __age_descriptive_table(self):
        descriptive_table = Descriptive_Table(vector_dict=self.continuous_vectors).get_descriptive_table()
        return descriptive_table

    def __age_vector_histograms(self):
        for vec in self.continuous_vectors:
            histogram(vector=self.continuous_vectors[vec],
                      label=vec,
                      x_label='age',
                      y_label='count',
                      add_mean_line=True,
                      path=self.local_output_path)

    def __age_vector_bar_plots(self):
        pass

    def __age_cross_tab_with_covid(self):
        pass
