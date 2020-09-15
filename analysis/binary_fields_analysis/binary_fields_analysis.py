import os
import numpy as np

from typing import List, Dict
from collections import defaultdict

from data_operations.build_ndarray_from_objects import build_nd_array_from_objects
from data_operations.data_frame_printer import Data_Frame_Printer
from analysis_operations.crosstab import Cross_Tab_Binary
from analysis_operations.graph_functions import bar_chart

from config.config import Config
from data.data_fields import Data_Fields


class Binary_Fields_Analysis:
    def __init__(self, patients: List, publish_results: bool):
        self.patients = patients
        self.publish_results = publish_results
        self.local_output_path = os.path.join(Config.OUTPUT_PATH, 'binary_fields_analysis')
        self.vectors: Dict[str: np.ndarray]

        self.__binary_fields_frequency_table: Dict or None = None
        self.__binary_fields_by_target_table: Dict or None = None

    def run_analysis(self):
        self.__binary_fields_frequency()
        self.__binary_field_bar_chart()
        self.__binary_fields_by_target()

        if self.publish_results:
            self.__publish_results_to_file()

    def __binary_fields_frequency(self):
        self.__build_vectors(remove_missing_values=True)

        data_dict = defaultdict(list)
        for field in self.vectors:
            positive_percent = self.vectors[field].mean()
            negative_percent = 1 - positive_percent

            total_patients = len(self.vectors[field])
            positive_count = total_patients * positive_percent
            negative_count = total_patients * negative_percent
            missing_count = len(self.patients) - total_patients

            data_dict['data_field'].append(field)
            data_dict['positive_percent'].append(positive_percent)
            data_dict['negative_percent'].append(negative_percent)
            data_dict['positive_count'].append(positive_count)
            data_dict['negative_count'].append(negative_count)
            data_dict['missing_count'].append(missing_count)

        self.__binary_fields_frequency_table = data_dict

    def __binary_field_bar_chart(self):
        bar_chart(x=self.__binary_fields_frequency_table['data_field'],
                  height=self.__binary_fields_frequency_table['positive_percent'],
                  title='binary_fields_frequency',
                  x_label='binary_fields',
                  y_label='%',
                  path=os.path.join(self.local_output_path))

    def __binary_fields_by_target(self):
        self.__build_vectors(remove_missing_values=False)
        target_vector = self.vectors[Data_Fields.get_target()]
        report_dict = defaultdict(list)

        for field in Data_Fields.get_binary_vars():
            vector = self.vectors[field]
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

        self.__binary_fields_by_target_table = report_dict

    def __build_vectors(self, remove_missing_values: bool):
        binary_fields = Data_Fields.get_binary_vars()
        vector_dict = {}

        for field in binary_fields:
            vector = build_nd_array_from_objects(object_list=self.patients,
                                                 field_name=field,
                                                 remove_missing_values=remove_missing_values)
            vector_dict[field] = vector
        self.vectors = vector_dict

    def __publish_results_to_file(self):
        df_printer = Data_Frame_Printer(path=self.local_output_path)
        df_printer.print_df_from_defaultdict(default_dict=self.__binary_fields_frequency_table,
                                             file_name='binary_fields_frequency_table.csv')

        df_printer.print_df_from_defaultdict(default_dict=self.__binary_fields_by_target_table,
                                             file_name='binary_fields_by_target_table.csv')
