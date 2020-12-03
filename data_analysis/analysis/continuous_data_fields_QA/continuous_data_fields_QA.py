from collections import defaultdict, Counter
from typing import Dict, List

from common_files.data_classes.data_fields import Data_Fields
from common_files.data_classes.patient import Patient

from config.data_analysis_config import Data_Analysis_Config as Config


class continuous_data_fields_QA:
    def __init__(self, patients: List[Patient]):
        self.__patients = patients
        self.__fields_in_qa: List[str] = Data_Fields.get_continuous_vars()
        self.report_tables: Dict = {}

        self.__calc()

    def __calc(self):
        self.__calc_QA()
        self.__replace_un_accepted_vital_values_with_none()

    def __calc_QA(self):
        un_accepted_values_frequency = defaultdict(list)

        for field_name in self.__fields_in_qa:
            counter = Counter()

            for patient in self.__patients:
                vital_value = getattr(patient, field_name)
                age_group = patient.age_group
                lower_threshold, upper_threshold = self.__calc_thresholds(age_group, field_name)

                if not vital_value:
                    counter['missing_values_count'] += 1
                elif vital_value > upper_threshold:
                    counter['points_higher_than_higher'] += 1
                elif vital_value < lower_threshold:
                    counter['points_lower_than_lower'] += 1
                else:
                    counter['points_in_accepted_range'] += 1

            missing_values_count = counter['missing_values_count']
            valid_points = len(self.__patients) - missing_values_count
            points_in_accepted_range = counter['points_in_accepted_range']
            points_lower_than_lower = counter['points_lower_than_lower']
            points_higher_than_higher = counter['points_higher_than_higher']

            un_accepted_values_frequency['field_name'].append(field_name)
            un_accepted_values_frequency['total_data_points'].append(len(self.__patients))
            un_accepted_values_frequency['missing_values_count'].append(missing_values_count)
            un_accepted_values_frequency['valid_points'].append(valid_points)
            un_accepted_values_frequency['points_in_accepted_range'].append(points_in_accepted_range / valid_points)
            un_accepted_values_frequency['points_lower_than_lower'].append(points_lower_than_lower / valid_points)
            un_accepted_values_frequency['points_higher_than_higher'].append(points_higher_than_higher / valid_points)

        self.report_tables['vitals_un_accepted_values_frequency'] = dict(un_accepted_values_frequency)

    @staticmethod
    def __calc_thresholds(age_group: str, field_name: str):
        lower_threshold = Config.get_continuous_field_threshold(age_group=age_group,
                                                                threshold='lower_threshold',
                                                                vital_value_name=field_name)

        upper_threshold = Config.get_continuous_field_threshold(age_group=age_group,
                                                                threshold='upper_threshold',
                                                                vital_value_name=field_name)

        return lower_threshold, upper_threshold

    def __replace_un_accepted_vital_values_with_none(self):
        for patient in self.__patients:
            age_group = patient.age_group

            for field_name in self.__fields_in_qa:
                vital_value = getattr(patient, field_name)

                if vital_value is None:
                    continue

                lower_threshold = Config.get_continuous_field_threshold(age_group=age_group,
                                                                        threshold='lower_threshold',
                                                                        vital_value_name=field_name)

                upper_threshold = Config.get_continuous_field_threshold(age_group=age_group,
                                                                        threshold='upper_threshold',
                                                                        vital_value_name=field_name)

                if vital_value > upper_threshold or vital_value < lower_threshold:
                    setattr(patient, field_name, None)
