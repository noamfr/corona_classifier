import pandas as pd
import os
from collections import defaultdict

from configuration.config import Config


class Pre_Analysis_Api:

    def __init__(self, raw_df: pd.DataFrame):
        self.raw_df = raw_df
        self.output_path = os.path.join(Config.OUTPUT_PATH, 'pre_analysis')

    def run_pre_analysis(self):
        self.__generate_descriptive_table()
        self.__missing_values_analysis()

    def __missing_values_analysis(self):
        missing_values_dict = defaultdict(list)
        total_rows = self.raw_df.shape[0]

        for column_name in self.raw_df.columns:
            null_count = self.raw_df[column_name].isnull().sum()
            null_percent = null_count / total_rows

            missing_values_dict['data_field'].append(column_name)
            missing_values_dict['null_count'].append(null_count)
            missing_values_dict['null_percent'].append(null_percent)

        missing_values_df = pd.DataFrame(missing_values_dict)
        missing_values_df.to_csv(os.path.join(self.output_path, 'missing_values_frequency_table.csv'))

    def __generate_descriptive_table(self):
        descriptive_table = round(self.raw_df.describe().T, 2)
        descriptive_table.to_csv(os.path.join(self.output_path, 'descriptive_table.csv'))

