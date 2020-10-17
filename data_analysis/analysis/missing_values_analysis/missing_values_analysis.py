import numpy as np
import os
from collections import defaultdict
from typing import List, Dict

from analysis_operations.descriptive_table import Descriptive_Table

from data.data_fields import Data_Fields
from data.patient import Patient


class Missing_Values_Analysis:

    def __init__(self, patients: List[Patient]):
        self.__patients = patients
        self.__report_tables: Dict = {}

        self.__run_analysis()

    def __run_analysis(self):
        self.__source_files_missing_values_analysis()
        self.__data_field_missing_values_analysis()
        self.__patient_missing_values_analysis()

    def __patient_missing_values_analysis(self):
        missing_values_counter = defaultdict(int)

        for patient in self.__patients:
            for data_field in Data_Fields.get_all_data_fields():
                if getattr(patient, data_field) is None:
                    missing_values_counter[patient.id] += 1

        patient_missing_values_vector = np.array([value for value in missing_values_counter.values()])
        descriptive_table = Descriptive_Table({'patient_missing_values_vector': patient_missing_values_vector})

        self.__report_tables['patient_missing_values_analysis'] = descriptive_table.get_descriptive_table()

        # histogram(path=self.local_output_path,
        #           vector=patient_missing_values_vector,
        #           label='patient_missing_values',
        #           x_label='missing values count',
        #           y_label='count',
        #           bins=patient_missing_values_vector.max(),
        #           x_ticks=range(0, patient_missing_values_vector.max() + 2, 2),
        #           add_mean_line=True)

    def __data_field_missing_values_analysis(self):
        missing_values_counter = dict(zip(Data_Fields.get_all_data_fields(),
                                          np.linspace(start=0, stop=0, num=len(Data_Fields.get_all_data_fields()))))

        for patient in self.__patients:
            for data_field in Data_Fields.get_all_data_fields():
                if getattr(patient, data_field) is None:
                    missing_values_counter[data_field] += 1

        total_patients = len(self.__patients)
        report_dict = defaultdict(list)
        for data_field in missing_values_counter:
            null_count = missing_values_counter[data_field]
            active_data_points_count = total_patients - missing_values_counter[data_field]
            null_percent = missing_values_counter[data_field] / total_patients
            active_data_points_percent = 1 - null_percent

            report_dict['data_field'].append(data_field)
            report_dict['null_count'].append(null_count)
            report_dict['active_data_points_count'].append(active_data_points_count)
            report_dict['null_percent'].append(null_percent)
            report_dict['active_data_percent'].append(active_data_points_percent)

        self.__report_tables['data_field_missing_values_analysis'] = report_dict

        # self.__bar_chart(x=df.data_field,
        #                  y=df.null_percent,
        #                  x_label='Data fields',
        #                  y_label='%',
        #                  title='missing_value_%',
        #                  output_path=self.local_output_path)

    def __source_files_missing_values_analysis(self):
        total_data_points_counter = {}
        missing_values_counter = {}

        for patient in self.__patients:
            source_file = patient.source_file

            if source_file not in total_data_points_counter.keys():
                total_data_points_counter[source_file] = 0
                missing_values_counter[source_file] = 0

            for idx in range(len(patient.__slots__)):
                total_data_points_counter[source_file] += 1

                value = getattr(patient, patient.__slots__[idx])
                if value is None:
                    missing_values_counter[source_file] += 1

        report_dict = defaultdict(list)
        total_data_points = 0
        total_missing_values = 0

        for source_file in total_data_points_counter:
            source_file_total_data_points = total_data_points_counter[source_file]
            source_file_missing_values_count = missing_values_counter[source_file]
            missing_values_percent = source_file_missing_values_count / source_file_total_data_points

            total_data_points += source_file_total_data_points
            total_missing_values += source_file_missing_values_count

            report_dict['source_file'].append(source_file)
            report_dict['total_data_points'].append(source_file_total_data_points)
            report_dict['missing_values_count'].append(source_file_missing_values_count)
            report_dict['missing_values_percent'].append(missing_values_percent)

        report_dict['source_file'].append('total')
        report_dict['total_data_points'].append(total_data_points)
        report_dict['missing_values_count'].append(total_missing_values)
        report_dict['missing_values_percent'].append(total_missing_values / total_data_points)

        self.__report_tables['source_files_missing_values_analysis'] = report_dict
        #
        # self.__bar_chart(x=df.source_file,
        #                  y=df.missing_values_percent,
        #                  x_label='Source Files',
        #                  y_label='%',
        #                  title='Source Files_missing_values_%',
        #                  output_path=self.local_output_path)

    @property
    def get_report_tables(self):
        return self.__report_tables

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
