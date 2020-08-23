import os
from statistics import mean
import pandas as pd
from collections import defaultdict
from config.config import Config
from get_data.data_fields import Data_Fields
from infra.graph_operations import bar_chart
from infra.data_operations import remove_missing_values_from_array


class Basic_Analysis:
    def __init__(self, patients):
        self.patients = patients
        self.local_output_path = os.path.join(Config.OUTPUT_PATH, 'basic_analysis')

    def calc(self):
        self.__binary_fields_frequency()

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

        df = pd.DataFrame(data_dict)
        df.to_csv(os.path.join(self.local_output_path, 'binary_fields_frequency.csv'))

        bar_chart(x=df.data_field,
                  y=df.positive_percent,
                  x_label='data field',
                  y_label='positive %',
                  title='binary_fields_frequency',
                  output_path=self.local_output_path)

    def __binary_fields_by_target(self):
        pass
