import os
import numpy as np
import pandas as pd
import seaborn as sns
from collections import defaultdict
from matplotlib import pyplot as plt
from typing import List, Dict

from analysis_operations.descriptive_table import Descriptive_Table

from data_classes.data_fields import Data_Fields
from data_classes.analysis_vector import Analysis_Vector
from config.data_analysis_config import Data_Analysis_Config as Config


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
        self.__average_by_target_for_age_groups()
        # self.__correlation_matrix()

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

    def __average_by_target_for_age_groups(self):
        report_table = defaultdict(list)

        vector_dict = self.__get_analysis_vector_dict()

        for continuous_var in Data_Fields.get_continuous_vars():
            if continuous_var == 'age':
                continue

            same_length_vectors = self.__get_same_length_vectors(vector_list=[vector_dict[Data_Fields.get_target()],
                                                                              vector_dict[Data_Fields.AGE.field_name],
                                                                              vector_dict[continuous_var]
                                                                              ])

            is_adult = same_length_vectors[Data_Fields.AGE.field_name] >= 18

            target_adult_vector = same_length_vectors[Data_Fields.get_target()][is_adult]
            response_adult_vector = same_length_vectors[continuous_var][is_adult]

            target_child_vector = same_length_vectors[Data_Fields.get_target()][~is_adult]
            response_child_vector = same_length_vectors[continuous_var][~is_adult]

            adult_corona_positive_response_vector = response_adult_vector[target_adult_vector == 1]
            adult_corona_negative_response_vector = response_adult_vector[target_adult_vector == 0]
            child_corona_positive_response_vector = response_child_vector[target_child_vector == 1]
            child_corona_negative_response_vector = response_child_vector[target_child_vector == 0]

            adult_bootstrap_significance = self.bootstrap_difference_in_mean_of_two_groups(
                adult_corona_positive_response_vector,
                adult_corona_negative_response_vector)

            child_bootstrap_significance = self.bootstrap_difference_in_mean_of_two_groups(
                child_corona_positive_response_vector,
                child_corona_negative_response_vector)

            adult_corona_positive_bootstrap_mean = self.__calc_bootstrap_mean(adult_corona_positive_response_vector,
                                                                              iterations=Config.BOOTSTRAP_ITERATIONS)

            adult_corona_negative_bootstrap_mean = self.__calc_bootstrap_mean(adult_corona_negative_response_vector,
                                                                              iterations=Config.BOOTSTRAP_ITERATIONS)

            child_corona_positive_bootstrap_mean = self.__calc_bootstrap_mean(child_corona_positive_response_vector,
                                                                              iterations=Config.BOOTSTRAP_ITERATIONS)

            child_corona_negative_bootstrap_mean = self.__calc_bootstrap_mean(child_corona_negative_response_vector,
                                                                              iterations=Config.BOOTSTRAP_ITERATIONS)

            adult_count = len(adult_corona_positive_response_vector) + len(adult_corona_negative_response_vector)
            child_count = len(child_corona_positive_response_vector) + len(child_corona_negative_response_vector)

            report_table['feature'].append(continuous_var)
            report_table['adult corona positive regular AVG'].append(np.mean(adult_corona_positive_response_vector))
            report_table['adult corona negative regular AVG'].append(np.mean(adult_corona_negative_response_vector))
            report_table['adult corona positive bootstrap AVG'].append(adult_corona_positive_bootstrap_mean)
            report_table['adult corona negative bootstrap AVG'].append(adult_corona_negative_bootstrap_mean)
            report_table['adult bootstrap significance'].append(adult_bootstrap_significance)
            report_table['adult count'].append(adult_count)

            report_table['child corona positive AVG'].append(np.mean(child_corona_positive_response_vector))
            report_table['child corona negative AVG'].append(np.mean(child_corona_negative_response_vector))
            report_table['child corona positive bootstrap AVG'].append(child_corona_positive_bootstrap_mean)
            report_table['child corona negative bootstrap AVG'].append(child_corona_negative_bootstrap_mean)
            report_table['child bootstrap significance'].append(child_bootstrap_significance)
            report_table['child count'].append(child_count)

        self.__report_tables['average_by_target'] = report_table

    @staticmethod
    def bootstrap_difference_in_mean_of_two_groups(vector_1: np.ndarray, vector_2: np.ndarray):
        v1_bigger_than_v2_count = 0
        for idx in range(Config.BOOTSTRAP_ITERATIONS):

            vector_1_random = np.random.choice(a=vector_1, size=round(len(vector_1) * 0.75))
            vector_2_random = np.random.choice(a=vector_2, size=round(len(vector_2) * 0.75))
            v1_mean = vector_1_random.mean()
            v2_mean = vector_2_random.mean()

            if v1_mean > v2_mean:
                v1_bigger_than_v2_count += 1

        v1_bigger_than_v2_ratio = v1_bigger_than_v2_count / Config.BOOTSTRAP_ITERATIONS
        significance_metric = abs(v1_bigger_than_v2_ratio - 0.5) + 0.5
        return significance_metric

    @staticmethod
    def __calc_bootstrap_mean(vector: np.ndarray, iterations: int):
        means = []

        for idx in range(iterations):
            vector_random = np.random.choice(a=vector, size=round(len(vector) * 0.75))
            means.append(np.mean(vector_random))
            return np.mean(means)

    def __get_same_length_vectors(self, vector_list: List[Analysis_Vector]):
        same_length_vectors = {}
        aggregated_missing_idx = self.__get_aggregated_missing_idx(vector_list=vector_list)

        for analysis_vector in vector_list:
            same_length_vector = np.delete(analysis_vector.vector, aggregated_missing_idx)
            same_length_vectors[analysis_vector.field_name] = same_length_vector
        return same_length_vectors

    @staticmethod
    def __get_aggregated_missing_idx(vector_list: List[Analysis_Vector]):
        aggregated_missing_idx = set()
        for vector in vector_list:
            aggregated_missing_idx.update(vector.missing_values_idx)

        return list(aggregated_missing_idx)

    def __get_analysis_vector_dict(self):
        vector_dict = {}
        for analysis_vector in self.__vectors:
            vector_dict[analysis_vector.field_name] = analysis_vector
        return vector_dict

    def __correlation_matrix(self):
        same_length_vectors = self.__get_same_length_vectors(vector_list=self.__vectors)
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

    @property
    def get_report_tables(self):
        return self.__report_tables

    @property
    def get_graph_vectors(self):
        return self.__graph_vectors
