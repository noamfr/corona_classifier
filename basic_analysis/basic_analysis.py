import os
from statistics import mean
import pandas as pd
from collections import defaultdict, Counter
from config.config import Config
from get_data.data_fields import Data_Fields
from infra.graph_operations import bar_chart
from infra.data_operations import remove_missing_values_from_array
from .crosstab import Cross_Tab_Binary


class Basic_Analysis:
    def __init__(self, patients):
        self.patients = patients
        self.local_output_path = os.path.join(Config.OUTPUT_PATH, 'basic_analysis')
        self.binary_data_fields_arrays = None

    def calc(self):
        self.__binary_fields_frequency()
        self.__binary_fields_by_target()

    def __binary_fields_frequency(self):
        binary_data_fields_arrays = {}

        for field in Data_Fields.get_binary_vars():
            binary_data_fields_arrays[field] = [getattr(patient, field) for patient in self.patients]
            if None in binary_data_fields_arrays[field]:
                binary_data_fields_arrays[field] = remove_missing_values_from_array(binary_data_fields_arrays[field])

        data_dict = defaultdict(list)
        for field in binary_data_fields_arrays:
            positive_percent = mean(binary_data_fields_arrays[field])
            negative_percent = 1 - positive_percent

            total_patients = len(binary_data_fields_arrays[field])
            positive_count = total_patients * positive_percent
            negative_count = total_patients * negative_percent
            missing_count = len(self.patients) - total_patients

            data_dict['data_field'].append(field)
            data_dict['positive_percent'].append(positive_percent)
            data_dict['negative_percent'].append(negative_percent)
            data_dict['positive_count'].append(positive_count)
            data_dict['negative_count'].append(negative_count)
            data_dict['missing_count'].append(missing_count)

        self.binary_data_fields_arrays = binary_data_fields_arrays
        df = pd.DataFrame(data_dict)
        df.to_csv(os.path.join(self.local_output_path, 'binary_fields_frequency.csv'))

        bar_chart(x=df.data_field,
                  y=df.positive_percent,
                  x_label='data field',
                  y_label='positive %',
                  title='binary_fields_frequency',
                  output_path=self.local_output_path)

    def __binary_fields_by_target(self):
        report_dict = defaultdict(list)

        target = Data_Fields.get_target()
        binary_data_fields = Data_Fields.get_binary_vars()
        binary_data_fields.remove(target)

        target_array = [getattr(patient, target) for patient in self.patients]

        for field in binary_data_fields:
            vector = [getattr(patient, field) for patient in self.patients]
            cross_tab = Cross_Tab_Binary(vector_1=target_array, vector_2=vector)

            field_positive_corona_positive_count = cross_tab.get_cross_tab_count(v1_binary_value=1, v2_binary_value=1)
            field_positive_corona_negative_count = cross_tab.get_cross_tab_count(v1_binary_value=0, v2_binary_value=1)
            field_negative_corona_positive_count = cross_tab.get_cross_tab_count(v1_binary_value=1, v2_binary_value=0)
            field_negative_corona_negative_count = cross_tab.get_cross_tab_count(v1_binary_value=0, v2_binary_value=0)
            missing_values_count = cross_tab.v2_missing_count

            field_positive_corona_positive_percent = cross_tab.get_cross_tab_percent(v1_binary_value=1, v2_binary_value=1)
            field_positive_corona_negative_percent = cross_tab.get_cross_tab_percent(v1_binary_value=0, v2_binary_value=1)
            field_negative_corona_positive_percent = cross_tab.get_cross_tab_percent(v1_binary_value=1, v2_binary_value=0)
            field_negative_corona_negative_percent = cross_tab.get_cross_tab_percent(v1_binary_value=0, v2_binary_value=0)

            corona_positive_percent_for_field_positives = cross_tab.get_perc_v1_positive_from_all_v2_positives()
            corona_positive_percent_for_field_negatives = cross_tab.get_perc_v1_positive_from_all_v2_negatives()

            report_dict['field'].append(field)
            report_dict['field_pos_corona_pos_count'].append(field_positive_corona_positive_count)
            report_dict['field_pos_corona_neg_count'].append(field_positive_corona_negative_count)
            report_dict['field_neg_corona_pos_count'].append(field_negative_corona_positive_count)
            report_dict['field_neg_corona_neg_count'].append(field_negative_corona_negative_count)
            report_dict['missing_values_count'].append(missing_values_count)

            report_dict['field_pos_corona_pos_percent'].append(field_positive_corona_positive_percent)
            report_dict['field_pos_corona_neg_percent'].append(field_positive_corona_negative_percent)
            report_dict['field_neg_corona_pos_percent'].append(field_negative_corona_positive_percent)
            report_dict['field_neg_corona_neg_percent'].append(field_negative_corona_negative_percent)

            report_dict['corona_pos_percent_for_field_positives'].append(corona_positive_percent_for_field_positives)
            report_dict['corona_pos_percent_for_field_negatives'].append(corona_positive_percent_for_field_negatives)

        df = pd.DataFrame(report_dict)
        df.to_csv(os.path.join(self.local_output_path, 'binary_fields_by_target.csv'))
