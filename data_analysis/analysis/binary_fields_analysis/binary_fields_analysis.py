import numpy as np
from typing import List, Dict
from collections import defaultdict

from data_operations.build_ndarray_from_objects import build_nd_array_from_object_list
from data.vector_builder import Analysis_Vector
from analysis_operations.crosstab import Cross_Tab_Binary

from data_analysis.data.data_fields import Data_Fields


class Binary_Fields_Analysis:
    def __init__(self, patients: List, vectors):
        self.__patients = patients
        self.__vectors: Dict[str: Analysis_Vector] = vectors
        self.__report_tables: Dict = {}

        self.__get_vectors_for_analysis()
        self.__run_analysis()

    def __run_analysis(self):
        self.__calc_frequency_table()
        # self.__calc_binary_fields_by_target()

    def __get_vectors_for_analysis(self):
        vectors_for_analysis = self.__vectors['target']
        vectors_for_analysis.update(self.__vectors['binary_vectors'])
        self.__vectors = vectors_for_analysis

    def __calc_frequency_table(self):
        report_dict = defaultdict(list)

        for field in self.__vectors:
            vector = self.__vectors[field].get_vector_without_missing_values()

            positive_percent = vector.mean()
            negative_percent = 1 - positive_percent

            total_patients = len(vector)
            positive_count = total_patients * positive_percent
            negative_count = total_patients * negative_percent
            missing_count = len(self.__vectors[field].vector) - total_patients

            report_dict['data_field'].append(field)
            report_dict['positive_percent'].append(positive_percent)
            report_dict['negative_percent'].append(negative_percent)
            report_dict['positive_count'].append(positive_count)
            report_dict['negative_count'].append(negative_count)
            report_dict['missing_count'].append(missing_count)

        self.__report_tables['binary_fields_frequency_table'] = report_dict

    def __calc_binary_fields_by_target(self):
        self.__build_vectors(remove_missing_values=False)
        target_vector = self.__vectors[Data_Fields.get_target()]
        report_dict = defaultdict(list)

        for field in Data_Fields.get_binary_vars():
            vector = self.__vectors[field]
            cross_tab = Cross_Tab_Binary(vector_1=target_vector, vector_2=vector)

            field_positive_corona_positive_count = cross_tab.get_cross_tab_count(v1_binary_value=1, v2_binary_value=1)
            field_positive_corona_negative_count = cross_tab.get_cross_tab_count(v1_binary_value=0, v2_binary_value=1)
            field_negative_corona_positive_count = cross_tab.get_cross_tab_count(v1_binary_value=1, v2_binary_value=0)
            field_negative_corona_negative_count = cross_tab.get_cross_tab_count(v1_binary_value=0, v2_binary_value=0)
            missing_values_count = cross_tab.v2_missing_count

            corona_positive_percent_for_field_positives = cross_tab.get_perc_v1_positive_from_all_v2_positives()
            corona_positive_percent_for_field_negatives = cross_tab.get_perc_v1_positive_from_all_v2_negatives()

            report_dict['field'].append(field)
            report_dict['field_pos_corona_pos_count'].append(field_positive_corona_positive_count)
            report_dict['field_pos_corona_neg_count'].append(field_positive_corona_negative_count)
            report_dict['field_neg_corona_pos_count'].append(field_negative_corona_positive_count)
            report_dict['field_neg_corona_neg_count'].append(field_negative_corona_negative_count)
            report_dict['missing_values_count'].append(missing_values_count)

            report_dict['corona_positive_and_field_positive'].append(corona_positive_percent_for_field_positives)
            report_dict['corona_positive_and_field_negative'].append(corona_positive_percent_for_field_negatives)

        self.__report_tables['binary_fields_by_target_table'] = report_dict

    @property
    def get_report_tables(self):
        return self.__report_tables

    def __build_vectors(self, remove_missing_values: bool):
        binary_fields = Data_Fields.get_binary_vars()
        vector_dict = {}

        for field in binary_fields:
            vector, idx_to_remove = build_nd_array_from_object_list(object_list=self.__patients,
                                                                    field_name=field,
                                                                    remove_missing_values=remove_missing_values)
            vector_dict[field] = vector
        self.__vectors = vector_dict

    # function for calculating binary unique values for one hot encoding
    def __calc_binary_unique_values(self):
        binary_data_fields = Data_Fields.get_binary_vars()
        binary_vars_unique_values = defaultdict(set)
        for patient in self.__patients:
            for field in binary_data_fields:
                value = getattr(patient, field)
                binary_vars_unique_values[field].add(value)

        self.__report_tables['binary_vars_unique_values'] = binary_vars_unique_values
