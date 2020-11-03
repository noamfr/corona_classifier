import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from typing import List, Dict

from analysis_operations.descriptive_table import Descriptive_Table

from data_analysis.data.data_fields import Data_Fields
from data.vector_builder import Analysis_Vector
from config.config import Config


class Continuous_Fields_Analysis:
    def __init__(self, patients: List, vectors: List[Analysis_Vector]):
        self.__patients = patients
        self.__vectors = vectors
        self.__report_tables: Dict = {}
        self.__graph_vectors: Dict = {}

        self.__get_vectors_for_analysis()
        self.__run_analysis()

    def __run_analysis(self):
        self.__descriptive_table()
        # self.__correlation_matrix()
        self.__average_by_target()
        self.__continuous_fields_quality()

    def __get_vectors_for_analysis(self):
        data_fields_for_analysis = [Data_Fields.get_target()]
        data_fields_for_analysis.extend(Data_Fields.get_continuous_vars())

        vectors_for_analysis = []
        for vector in self.__vectors:
            if vector.field_name in data_fields_for_analysis:
                if vector.field_name in Config.DATA_FIELDS_IN_ANALYSIS:
                    vectors_for_analysis.append(vector)

        self.__vectors = vectors_for_analysis
        self.__graph_vectors['continuous_vectors'] = self.__vectors

    def __descriptive_table(self):
        vector_dict = self.__get_vector_dict(remove_missing_values=True)
        descriptive_table = Descriptive_Table(vector_dict=vector_dict)
        self.__report_tables['descriptive_table'] = descriptive_table.get_descriptive_table()

    def __get_vector_dict(self, remove_missing_values: bool):
        vector_dict = {}
        for analysis_vector in self.__vectors:
            field_name = analysis_vector.field_name
            if field_name == Data_Fields.get_target():
                continue

            if remove_missing_values:
                vector = analysis_vector.vector_without_missing_values
            else:
                vector = analysis_vector.vector
            vector_dict[field_name] = vector
        return vector_dict

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

    def __get_same_length_vectors(self):
        same_length_vectors = {}
        aggregated_missing_idx = self.__get_aggregated_missing_idx()

        for analysis_vector in self.__vectors:
            same_length_vector = np.delete(analysis_vector.vector, aggregated_missing_idx)
            same_length_vectors[analysis_vector.field_name] = same_length_vector

        return same_length_vectors

    def __get_aggregated_missing_idx(self):
        aggregated_missing_idx = set()
        for vector in self.__vectors:
            aggregated_missing_idx.update(vector.missing_values_idx)

        return aggregated_missing_idx

    def __average_by_target(self):
        pass

    def __continuous_fields_quality(self):
        pass

    @property
    def get_report_tables(self):
        return self.__report_tables

    @property
    def get_graph_vectors(self):
        return self.__graph_vectors
