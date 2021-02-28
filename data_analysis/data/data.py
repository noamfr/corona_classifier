from typing import List

from data_classes.data_reader import Data_Reader
from data_classes.data_fields import Data_Fields
from data_classes.patient import Patient
from data_classes.analysis_vector import Analysis_Vector_Builder, Analysis_Vector

from config.data_analysis_config import Data_Analysis_Config as Config


class Data:
    def __init__(self):
        self.patients: List[Patient] = []
        self.analysis_vectors: List[Analysis_Vector] = []

        self.__calc()

    def __calc(self):
        self.__fetch_patients()
        self.__replace_empty_strings_with_none()
        self.__binary_one_hot_encoding()
        self.__remove_data_fields_with_to_much_missing_data()
        self.__remove_patients_with_to_much_missing_values()
        self.__build_analysis_vectors()

    def __fetch_patients(self):
        data_reader = Data_Reader(raw_data_path=Config.RAW_DATA_PATH)
        self.patients = data_reader.patients

    def __replace_empty_strings_with_none(self):
        data_fields = Data_Fields.get_all_data_fields()
        for patient in self.patients:
            for data_field in data_fields:
                if getattr(patient, data_field) == '':
                    setattr(patient, data_field, None)

    def __binary_one_hot_encoding(self):
        binary_fields = Data_Fields.get_binary_vars()
        binary_fields.append(Data_Fields.get_target())

        for patient in self.patients:
            for field in binary_fields:
                if getattr(patient, field) is None:
                    continue
                elif getattr(patient, field) not in ('TRUE', 'Positive'):
                    setattr(patient, field, 0)
                else:
                    setattr(patient, field, 1)

    def __remove_data_fields_with_to_much_missing_data(self):
        for data_field in Data_Fields.get_all_data_fields():
            missing_data_count = 0
            for patient in self.patients:
                if getattr(patient, data_field) is None:
                    missing_data_count += 1

            missing_data_ratio = missing_data_count / len(self.patients)

            if missing_data_ratio >= Config.DATA_FIELD_MISSING_VALUES_THRESHOLD:
                Config.DATA_FIELDS_IN_ANALYSIS.remove(data_field)

    def __remove_patients_with_to_much_missing_values(self):
        idx_to_remove = set()
        for idx in range(len(self.patients)):
            missing_values_count = 0

            for data_field in Config.DATA_FIELDS_IN_ANALYSIS:
                if getattr(self.patients[idx], data_field) is None:
                    missing_values_count += 1

            if missing_values_count > Config.PATIENT_MISSING_VALUES_THRESHOLD:
                idx_to_remove.add(idx)

        idx_to_remove = sorted(idx_to_remove, reverse=True)
        for idx in idx_to_remove:
            self.patients.pop(idx)

    def __build_analysis_vectors(self):
        vector_builder = Analysis_Vector_Builder(data_object_list=self.patients,
                                                 data_fields=Data_Fields.get_all_data_fields())

        self.analysis_vectors = vector_builder.analysis_vectors
