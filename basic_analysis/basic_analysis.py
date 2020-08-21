import os
import statistics
import pandas as pd
from config.config import Config
from get_data.data_fields import Data_Fields
from infra.graph_operations import bar_chart


class Basic_Analysis:
    def __init__(self, patients):
        self.patients = patients
        self.local_output_path = os.path.join(Config.OUTPUT_PATH, 'basic_analysis')

    def calc(self):
        self.__target_frequency()

    def __target_frequency(self):
        target_field = Data_Fields.get_target()
        target_array = [getattr(patient, target_field) for patient in self.patients]

        total_patients = len(target_array)
        corona_positive_percent = statistics.mean(target_array)
        corona_negative_percent = 1 - corona_positive_percent

        corona_positive_count = total_patients * corona_positive_percent
        corona_negative_count = total_patients * corona_negative_percent

        status = ['corona_positive', 'corona_negative', 'total']
        percent = [corona_positive_percent, corona_negative_percent,
                   corona_positive_percent+corona_negative_percent]
        count = [corona_positive_count, corona_negative_count, total_patients]

        df = pd.DataFrame(list(zip(status, percent, count)),
                          columns=['status', 'percent', 'count'])

        df.to_csv(os.path.join(self.local_output_path,
                               'target_frequency.csv'))

        bar_chart(x=status[:-1],
                  y=percent[:-1],
                  x_label='corona_test_result',
                  y_label='%',
                  title='corona_test_result_frequency',
                  output_path=self.local_output_path)

    def __binary_fields_by_target(self):
        pass
