from typing import List
import numpy as np
import pandas as pd
import os
from collections import defaultdict
from config.config import Config, Static_Configs
from get_data.data_fields import Data_Fields
from data.data_field_remover import Data_field_remover


class Missing_Values:

    def __init__(self, patients: List):
        self.local_output_path = os.path.join(Config.OUTPUT_PATH, 'missing_values')
        self.__data_fields = Data_Fields
        self.__patients = patients
        self.data_field_missing_values = None

    def remove_data_fields_with_to_much_missing_data(self):
        self.__source_files_missing_values_analysis()
        self.__data_field_missing_value_analysis()
        self.__remove_fields()

    # def run_missing_value_analysis(self):
    #     self.__source_files_missing_values_analysis()
    #     self.__data_field_missing_value_analysis()

    def __data_field_missing_value_analysis(self):
        missing_values_counter = dict(zip(Data_Fields.get_all_data_fields(),
                                          np.linspace(start=0, stop=0, num=len(Data_Fields.get_all_data_fields()))))

        for patient in self.__patients:
            for data_field in Data_Fields.get_all_data_fields():
                if getattr(patient, data_field) is None:
                    missing_values_counter[data_field] += 1

        total_patients = len(self.__patients)
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

        self.data_field_missing_values = data_dict
        df = pd.DataFrame(data_dict)
        df.to_csv(os.path.join(self.local_output_path, 'missing_values_frequency_table_from_array.csv'))

        self.__bar_chart(x=df.data_field,
                         y=df.null_percent,
                         x_label='Data fields',
                         y_label='%',
                         title='missing_value_%',
                         output_path=self.local_output_path)

    def __source_files_missing_values_analysis(self):
        total_data_points_counter = {}
        missing_values_counter = {}

        for patient in self.__patients:
            source_file = patient.source_file

            if source_file not in total_data_points_counter.keys():
                total_data_points_counter[source_file] = 0
                missing_values_counter[source_file] = 0

            for idx in range(len(patient.__slotnames__)):
                total_data_points_counter[source_file] += 1

                value = getattr(patient, patient.__slotnames__[idx])
                if value is None:
                    missing_values_counter[source_file] += 1

        results = defaultdict(list)
        total_data_points = 0
        total_missing_values = 0

        for source_file in total_data_points_counter:
            source_file_total_data_points = total_data_points_counter[source_file]
            source_file_missing_values_count = missing_values_counter[source_file]
            missing_values_percent = source_file_missing_values_count / source_file_total_data_points

            total_data_points += source_file_total_data_points
            total_missing_values += source_file_missing_values_count

            results['source_file'].append(source_file)
            results['total_data_points'].append(source_file_total_data_points)
            results['missing_values_count'].append(source_file_missing_values_count)
            results['missing_values_percent'].append(missing_values_percent)

        results['source_file'].append('total')
        results['total_data_points'].append(total_data_points)
        results['missing_values_count'].append(total_missing_values)
        results['missing_values_percent'].append(total_missing_values / total_data_points)

        df = pd.DataFrame(results)
        df.to_csv(os.path.join(self.local_output_path, 'source_files_missing_values_analysis.csv'))

        self.__bar_chart(x=df.source_file,
                         y=df.missing_values_percent,
                         x_label='Source Files',
                         y_label='%',
                         title='Source Files_missing_values_%',
                         output_path=self.local_output_path)

    def __get_fields_not_in_analysis(self):
        data_fields_not_in_analysis = []
        for idx in range(len(self.data_field_missing_values['data_field'])):
            if self.data_field_missing_values['null_percent'][idx] >= Static_Configs.MISSING_VALUES_THRESHOLD:
                data_fields_not_in_analysis.append(self.data_field_missing_values['data_field'][idx])

        return data_fields_not_in_analysis

    def __remove_fields(self):
        data_field_remover = Data_field_remover(data_field_class=Data_Fields,
                                                fields_to_remove= self.__get_fields_not_in_analysis())
        data_field_remover.remove_date_fields()

    @staticmethod
    def __bar_chart(x, y, x_label: str, y_label: str, title: str, output_path: str):
        from matplotlib import pyplot as plt
        import seaborn as sns
        plt.clf()
        sns.set(style='darkgrid')
        sns.barplot(x=x, y=y, color='salmon')
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.ylim(0, 1)
        plt.title(title)
        plt.xticks(rotation=45, ha='right', fontsize=6, weight='bold')
        plt.tight_layout()
        # plt.figure(figsize=(5, 5))
        plt.savefig(fname=os.path.join(output_path, f'{title}.png'), dpi=300)
