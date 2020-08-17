import numpy as np
import pandas as pd
import math
import os
from collections import defaultdict
from configuration.config import Config
from get_data_layer.data_fields import Data_Fields


class Data_Api:

    def __init__(self, patients: list):
        self.local_output_path = os.path.join(Config.OUTPUT_PATH, 'pre_analysis')
        self.data_fields = Data_Fields
        self.patients = patients
        self.missing_values_counter = None
        self.data_fields_for_analysis = []
        self.prep_df: pd.DataFrame

    def run_missing_value_analysis(self):
        self.__patient_missing_value_analysis()

        # self.__data_frame_missing_value_comparison()
        # self.__missing_values_analysis()
        # self.__remove_data_fields_with_too_much_missing_values()
        # self.__binary_vars_value_counts_table()

    def __patient_missing_value_analysis(self):
        missing_values_counter = dict(zip(Data_Fields.get_all_data_fields(),
                                          np.linspace(start=0, stop=0, num=len(Data_Fields.get_all_data_fields()))))

        for patient in self.patients:
            for data_field in Data_Fields.get_all_data_fields():
                if getattr(patient, data_field) is None:
                    # if np.isnan(getattr(patient, data_field)):
                    missing_values_counter[data_field] += 1
        self.missing_values_counter = missing_values_counter

        total_patients = len(self.patients)
        data_dict = defaultdict(list)
        for data_field in missing_values_counter:
            null_count = missing_values_counter[data_field]
            active_data_points_count = total_patients - missing_values_counter[data_field]
            null_percent = missing_values_counter[data_field] / total_patients
            active_data_points_percent = 1 - null_percent

            data_dict['data_field'].append(data_field)
            data_dict['null_count'].append(null_count)
            data_dict['active_data_points_count'].append(active_data_points_count)
            data_dict['null_percent'].append(null_percent)
            data_dict['active_data_percent'].append(active_data_points_percent)

        df = pd.DataFrame(data_dict)
        df.to_csv(os.path.join(self.local_output_path, 'missing_values_frequency_table_from_array.csv'))

        self.__bar_chart(x=df.data_field,
                         y=df.null_percent,
                         x_label='Data fields',
                         y_label='%',
                         title='missing_value_%',
                         output_path=self.local_output_path)

    @staticmethod
    def __bar_chart(x, y, x_label: str, y_label: str, title: str, output_path: str):
        from matplotlib import pyplot as plt
        import seaborn as sns
        plt.clf()
        sns.set(style='darkgrid')
        sns.barplot(x=x, y=y, color='salmon')
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.xticks(rotation=45, ha='right', fontsize=8, weight='bold')
        plt.tight_layout()
        plt.savefig(fname=os.path.join(output_path, f'{title}.png'))

    def __source_files_missing_values_comparison(self):
        total_data_points_counter = {}
        missing_values_counter = {}

        for patient in self.patients:
            source_file = patient.source_file

            if source_file not in total_data_points_counter.keys():
                total_data_points_counter[source_file] = 0
                missing_values_counter[source_file] = 0

            # for key in



    def __data_frame_missing_value_comparison(self):
        source_dfs = set()
        for patient in self.patients:
            source_df = getattr(patient, Data_Fields.SOURCE_FILE.field_name)
            source_dfs.add(source_df)

        df_missing_values_counter = dict(zip(source_dfs, np.linspace(start=0, stop=0, num=len(source_dfs))))
        df_data_point_counter = dict(zip(source_dfs, np.linspace(start=0, stop=0, num=len(source_dfs))))

        for patient in self.patients:
            source_df = getattr(patient, Data_Fields.SOURCE_FILE.field_name)

            for data_field in patient.attribute_dict:
                df_data_point_counter[source_df] += 1
                if type(patient.attribute_dict[data_field]) in (float, np.float64):
                    if np.isnan(patient.attribute_dict[data_field]):
                        df_missing_values_counter[source_df] += 1

        missing_value_comparison_data_dict = defaultdict(list)
        for source_df in source_dfs:

            total_data_points = df_data_point_counter[source_df]
            total_missing_values = df_missing_values_counter[source_df]
            missing_values_percent = total_missing_values / total_data_points

            missing_value_comparison_data_dict['source_df'] = source_df
            missing_value_comparison_data_dict['total_data_points'] = total_data_points
            missing_value_comparison_data_dict['total_missing_values'] = total_missing_values
            missing_value_comparison_data_dict['missing_values_percent'] = missing_values_percent

        df_missing_value_comparison = pd.DataFrame(missing_value_comparison_data_dict)
        df_missing_value_comparison.to_csv(os.path.join(self.local_output_path, 'df_missing_value_comparison.csv'))

    def __missing_values_analysis(self):
        missing_values_dict = defaultdict(list)
        total_rows = self.raw_df.shape[0]

        for column_name in self.raw_df.columns:
            null_count = self.raw_df[column_name].isnull().sum()
            null_percent = null_count / total_rows
            active_data_points = total_rows - null_count

            missing_values_dict['data_field'].append(column_name)
            missing_values_dict['active_data_points'].append(active_data_points)
            missing_values_dict['null_count'].append(null_count)
            missing_values_dict['null_percent'].append(null_percent)

        missing_values_df = pd.DataFrame(missing_values_dict)
        self.missing_values_dict = missing_values_dict
        missing_values_df.to_csv(os.path.join(self.local_output_path, 'missing_values_frequency_table.csv'))
        self.data_fields.too_much_missing_data = False

    def __remove_data_fields_with_too_much_missing_values(self):
        data_fields_for_analysis = []

        for idx in range(len(self.missing_values_dict['data_field'])):
            if self.missing_values_dict['null_percent'][idx] < Config.get_missing_value_threshold():
                data_fields_for_analysis.append(self.missing_values_dict['data_field'][idx])

        self.data_fields_for_analysis = data_fields_for_analysis
        self.prep_df = self.raw_df[data_fields_for_analysis]

    def __binary_vars_value_counts_table(self):
        data_dict = defaultdict(list)
        for var_name in self.data_fields.get_binary_vars():
            if var_name not in self.data_fields_for_analysis:
                continue
            false_n = self.raw_df[var_name].value_counts()[0]
            true_n = self.raw_df[var_name].value_counts()[1]

            false_percent = self.raw_df[var_name].value_counts(normalize=True)[0]
            true_percent = self.raw_df[var_name].value_counts(normalize=True)[1]

            data_dict['data_field'].append(var_name)
            data_dict['false_n'].append(false_n)
            data_dict['true_n'].append(true_n)
            data_dict['false_percent'].append(false_percent)
            data_dict['true_percent'].append(true_percent)

        df = pd.DataFrame(data_dict)
        df.to_csv(os.path.join(self.local_output_path, 'binary_vars_value_counts_table.csv'))

    def __generate_descriptive_table(self):
        descriptive_table = round(self.raw_df.describe().T, 2)
        descriptive_table.to_csv(os.path.join(self.local_output_path, 'descriptive_table.csv'))

