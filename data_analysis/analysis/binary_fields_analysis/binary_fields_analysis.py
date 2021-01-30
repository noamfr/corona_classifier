from typing import List, Dict
from collections import defaultdict

from config.data_analysis_config import Data_Analysis_Config
from data_classes.analysis_vector import Analysis_Vector

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
                if vector.field_name in Data_Analysis_Config.DATA_FIELDS_IN_ANALYSIS:
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

            target_pos_feature_pos = 0
            target_pos_feature_neg = 0
            target_neg_feature_pos = 0
            target_neg_feature_neg = 0
            not_grouped = 0

            for idx in range(len(analysis_vector.vector)):
                feature_value = analysis_vector.vector[idx]
                target_value = target_vector.vector[idx]

                if feature_value is None or target_value is None:
                    continue

                elif target_value == 1 and feature_value == 1:
                    target_pos_feature_pos += 1

                elif target_value == 1 and feature_value == 0:
                    target_pos_feature_neg += 1

                elif target_value == 0 and feature_value == 1:
                    target_neg_feature_pos += 1

                elif target_value == 0 and feature_value == 0:
                    target_neg_feature_neg += 1

                else:
                    not_grouped += 0

            all_valid_tests = target_pos_feature_pos + target_pos_feature_neg + target_neg_feature_pos + target_neg_feature_neg

            feature_pos_within_covid_positive_tests = target_pos_feature_pos / (target_pos_feature_pos + target_pos_feature_neg)
            feature_pos_within_all_tests = (target_pos_feature_pos + target_neg_feature_pos) / all_valid_tests

            report_dict['feature'].append(analysis_vector.field_name)
            report_dict['feature positive within covid positive tests'].append(feature_pos_within_covid_positive_tests)
            report_dict['feature positive within all tests'].append(feature_pos_within_all_tests)
            report_dict['target positive feature positive'].append(target_pos_feature_pos)
            report_dict['target positive feature negative'].append(target_pos_feature_neg)
            report_dict['target negative feature positive'].append(target_neg_feature_pos)
            report_dict['target negative feature negative'].append(target_neg_feature_neg)
            report_dict['all valid tests'].append(all_valid_tests)

        self.__report_tables['binary_fields_by_target_table'] = dict(report_dict)

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
