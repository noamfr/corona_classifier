import os
import numpy as np
import pandas as pd
from typing import List, Dict

from data_operations.build_ndarray_from_objects import build_nd_array_from_object_list
from analysis_operations.descriptive_table import Descriptive_Table
from config.config import Config
from data.data_fields import Data_Fields


class Continuous_Fields_Analysis:
    def __init__(self, patients: List, publish_results: bool):
        self.patients = patients
        self.publish_results = publish_results
        self.local_output_path = os.path.join(Config.OUTPUT_PATH, 'continuous_fields_analysis')
        self.vectors: Dict[str: np.ndarray]
        self.descriptive_table = None

        self.__build_vectors(remove_missing_values=True)

    def run_analysis(self):
        self.__descriptive_table()
        self.__correlation_matrix()

        if self.publish_results:
            self.__publish_results_to_file()

    def __descriptive_table(self):
        descriptive_table = Descriptive_Table(vector_dict=self.vectors)
        self.descriptive_table = descriptive_table.get_descriptive_table()

    def __correlation_matrix(self):
        df = pd.DataFrame(self.vectors)

        corr = df.corr()
        corr.style.background_gradient(cmap='coolwarm')

    def __average_by_target(self):
        pass

    def __build_vectors(self, remove_missing_values: bool):
        continuous_fields = Data_Fields.get_continuous_vars()
        vector_dict = {}

        for field in continuous_fields:
            vector = build_nd_array_from_object_list(object_list=self.patients,
                                                     field_name=field,
                                                     remove_missing_values=remove_missing_values)
            vector_dict[field] = vector
        self.vectors = vector_dict

    def __publish_results_to_file(self):
        descriptive_table_df = pd.DataFrame(self.descriptive_table)
        descriptive_table_df.to_csv(os.path.join(self.local_output_path, 'descriptive_table.csv'))
