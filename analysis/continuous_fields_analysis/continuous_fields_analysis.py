import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from typing import List, Dict
from collections import defaultdict

from ..analysis_vector import Analysis_Vector

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
        self.missing_value_idx_for_vectors: Dict

        self.descriptive_table = None

        self.__build_vectors(remove_missing_values=True)

    def run_analysis(self):
        self.__descriptive_table()
        self.__correlation_matrix()
        self.__average_by_target()

        if self.publish_results:
            self.__publish_results_to_file()

    def __descriptive_table(self):
        vector_dict = dict(zip([getattr(vector, 'field_name') for vector in self.vectors],
                               [getattr(vector, 'vector') for vector in self.vectors]))

        descriptive_table = Descriptive_Table(vector_dict=vector_dict)
        self.descriptive_table = descriptive_table.get_descriptive_table()

    def __correlation_matrix(self):
        same_length_vectors = self.__get_same_length_vectors()
        df = pd.DataFrame(same_length_vectors)

        corr = df.corr()
        corr.style.background_gradient(cmap='coolwarm')

        plt.clf()
        sns.heatmap(round(corr, 2), annot=True, square=True, cmap='RdBu', vmin=-1, vmax=1, linewidth=0.5)
        plt.xticks(np.arange(df.shape[1]), df.columns, fontsize=10, rotation=35, fontweight='bold')
        plt.yticks(np.arange(df.shape[1]) + 0.5, df.columns, fontsize=10, va="center", fontweight='bold')
        plt.title('Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(self.local_output_path, 'correlation_matrix.png'))

    def __average_by_target(self):
        continuous_fields = Data_Fields.get_continuous_vars()

    def __build_vectors(self, remove_missing_values: bool):
        continuous_fields = Data_Fields.get_continuous_vars()
        vectors = []
        missing_value_idx_for_vectors = {}

        for field in continuous_fields:
            vector, missing_value_idx = build_nd_array_from_object_list(object_list=self.patients,
                                                                        field_name=field,
                                                                        remove_missing_values=remove_missing_values)

            vector = Analysis_Vector(field_name=field, vector=vector, missing_value_idx=missing_value_idx)
            vectors.append(vector)
            missing_value_idx_for_vectors[field] = missing_value_idx

        self.vectors = vectors
        self.missing_value_idx_for_vectors = missing_value_idx_for_vectors

    def __get_aggregated_missing_idx(self):
        aggregated_missing_idx = set()
        for vector in self.missing_value_idx_for_vectors:
            aggregated_missing_idx.update(self.missing_value_idx_for_vectors[vector])

        return aggregated_missing_idx

    def __get_same_length_vectors(self):
        continuous_fields = Data_Fields.get_continuous_vars()
        # continuous_fields.remove('days_since_symptom_onset')

        vectors = {}

        for field in continuous_fields:
            vector, missing_value_idx = build_nd_array_from_object_list(object_list=self.patients,
                                                                        field_name=field,
                                                                        remove_missing_values=False)
            vectors[field] = vector

        same_length_vectors = {}
        aggregated_missing_idx = list(self.__get_aggregated_missing_idx())

        for field in vectors:
            vector = np.delete(vectors[field], aggregated_missing_idx)
            same_length_vectors[field] = vector

        return same_length_vectors


    def __publish_results_to_file(self):
        descriptive_table_df = pd.DataFrame(self.descriptive_table)
        descriptive_table_df.to_csv(os.path.join(self.local_output_path, 'descriptive_table.csv'))
