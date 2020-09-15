import os
import numpy as np
from typing import List, Dict

from data_operations.build_ndarray_from_objects import build_nd_array_from_objects
from data_operations.data_frame_printer import Data_Frame_Printer
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

    def run_analysis(self):
        self.__continuous_fields_descriptive_table()

        if self.publish_results:
            self.__publish_results_to_file()

    def __continuous_fields_descriptive_table(self):
        self.__build_vectors(remove_missing_values=False)
        self.descriptive_table = Descriptive_Table(vector_dict=self.vectors)

    def __build_vectors(self, remove_missing_values: bool):
        continuous_fields = Data_Fields.get_continuous_vars()
        vector_dict = {}

        for field in continuous_fields:
            vector = build_nd_array_from_objects(object_list=self.patients,
                                                 field_name=field,
                                                 remove_missing_values=remove_missing_values)
            vector_dict[field] = vector
        self.vectors = vector_dict

    def __publish_results_to_file(self):
        df_printer = Data_Frame_Printer(path=self.local_output_path)
        df_printer.print_df_from_defaultdict(default_dict=self.descriptive_table,
                                             file_name='descriptive_table.csv')
