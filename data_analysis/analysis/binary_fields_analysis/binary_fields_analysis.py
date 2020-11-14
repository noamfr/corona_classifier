from typing import List, Dict
from collections import defaultdict

from config.analysis_config import Analysis_Config
from data_classes.analysis_vector import Analysis_Vector
from analysis_operations.crosstab import Cross_Tab_Binary

from data_classes.data_fields import Data_Fields


class Binary_Fields_Analysis:
    def __init__(self, patients: List, vectors):
        self.__patients = patients
        self.__vectors: List[Analysis_Vector] = vectors
        self.__report_tables: Dict = {}

        self.__get_vectors_for_analysis()
        self.__run_analysis()

    def __run_analysis(self):
        self.__calc_frequency_table()
        self.__calc_binary_fields_by_target()

    def __get_vectors_for_analysis(self):
        data_fields_for_analysis = [Data_Fields.get_target()]
        data_fields_for_analysis.extend(Data_Fields.get_binary_vars())

        vectors_for_analysis = []
        for vector in self.__vectors:
            if vector.field_name in data_fields_for_analysis:
                if vector.field_name in Analysis_Config.DATA_FIELDS_IN_ANALYSIS:
                    vectors_for_analysis.append(vector)

        self.__vectors = vectors_for_analysis

    def __calc_frequency_table(self):
        report_dict = defaultdict(list)

        for analysis_vector in self.__vectors:
            clean_vector = analysis_vector.vector_without_missing_values
            positive_percent = clean_vector.mean()
            negative_percent = 1 - positive_percent

            total_valid_patients = len(clean_vector)
            positive_count = total_valid_patients * positive_percent
            negative_count = total_valid_patients * negative_percent
            missing_count = analysis_vector.get_missing_values_count

            report_dict['data_field'].append(analysis_vector.field_name)
            report_dict['positive_percent'].append(positive_percent)
            report_dict['negative_percent'].append(negative_percent)
            report_dict['positive_count'].append(positive_count)
            report_dict['negative_count'].append(negative_count)
            report_dict['missing_count'].append(missing_count)

        self.__report_tables['binary_fields_frequency_table'] = report_dict

    def __calc_binary_fields_by_target(self):
        report_dict = defaultdict(list)
        target_vector = self.__get_single_vector(Data_Fields.get_target())

        for analysis_vector in self.__vectors:
            if analysis_vector.field_name == Data_Fields.get_target():
                continue

            cross_tab = Cross_Tab_Binary(vector_1=target_vector.vector, vector_2=analysis_vector.vector)
            field_positive_corona_positive_count = cross_tab.get_cross_tab_count(v1_binary_value=1, v2_binary_value=1)
            field_positive_corona_negative_count = cross_tab.get_cross_tab_count(v1_binary_value=0, v2_binary_value=1)
            field_negative_corona_positive_count = cross_tab.get_cross_tab_count(v1_binary_value=1, v2_binary_value=0)
            field_negative_corona_negative_count = cross_tab.get_cross_tab_count(v1_binary_value=0, v2_binary_value=0)
            missing_values_count = cross_tab.v2_missing_count
            corona_positive_percent_for_field_positives = cross_tab.get_perc_v1_positive_from_all_v2_positives()
            corona_positive_percent_for_field_negatives = cross_tab.get_perc_v1_positive_from_all_v2_negatives()

            report_dict['field'].append(analysis_vector.field_name)
            report_dict['corona_positive_and_field_positive'].append(corona_positive_percent_for_field_positives)
            report_dict['corona_positive_and_field_negative'].append(corona_positive_percent_for_field_negatives)

            report_dict['field_pos_corona_pos_count'].append(field_positive_corona_positive_count)
            report_dict['field_pos_corona_neg_count'].append(field_positive_corona_negative_count)
            report_dict['field_neg_corona_pos_count'].append(field_negative_corona_positive_count)
            report_dict['field_neg_corona_neg_count'].append(field_negative_corona_negative_count)
            report_dict['missing_values_count'].append(missing_values_count)

        self.__report_tables['binary_fields_by_target_table'] = report_dict

    def __get_single_vector(self, vector_name: str):
        for analysis_vector in self.__vectors:
            if analysis_vector.field_name == vector_name:
                return analysis_vector

    @property
    def get_report_tables(self):
        return self.__report_tables

    # function for calculating binary unique values before one hot encoding

    def __calc_binary_unique_values(self):
        binary_data_fields = Data_Fields.get_binary_vars()
        binary_vars_unique_values = defaultdict(set)
        for patient in self.__patients:
            for field in binary_data_fields:
                value = getattr(patient, field)
                binary_vars_unique_values[field].add(value)

        self.__report_tables['binary_vars_unique_values'] = binary_vars_unique_values
