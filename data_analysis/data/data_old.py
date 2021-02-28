from typing import List

from data_classes.data_reader import Data_Reader
from data_classes.data_fields import Data_Fields
from data_classes.patient import Patient
from data_classes.analysis_vector import Analysis_Vector_Builder, Analysis_Vector

from config.data_analysis_config import Data_Analysis_Config as Config


class Data_Old:
    def __init__(self, remove_missing_values=False):
        self.__remove_missing_values = remove_missing_values
        self.__patients: List[Patient] = []
        self.__vectors: List[Analysis_Vector] = []

        self.__calc()

    def __calc(self):
        self.__fetch_patients()
        self.__remove_patients_with_too_much_missing_data()
        self.__binary_one_hot_encoding()
        self.__build_analysis_vectors()

        if self.__remove_missing_values:
            self.__remove_data_fields_with_to_much_missing_data()

    def __fetch_patients(self):
        data_reader = Data_Reader(raw_data_path=Config.RAW_DATA_PATH)
        self.__patients = data_reader.get_patients_old()

    def __remove_patients_with_too_much_missing_data(self):
        patient_idx_to_remove = []
        for idx in range(len(self.__patients)):
            missing_value_count = 0

            for slot in self.__patients[idx].__slots__:
                if getattr(self.__patients[idx], slot) is None:
                    missing_value_count += 1

            if missing_value_count > Config.PATIENT_MISSING_VALUES_THRESHOLD:
                patient_idx_to_remove.append(idx)

        patient_idx_to_remove.sort(reverse=True)
        for idx in patient_idx_to_remove:
            self.__patients.pop(idx)

    def __binary_one_hot_encoding(self):
        data_fields = Data_Fields.get_binary_vars()
        data_fields.append(Data_Fields.get_target())

        for patient in self.__patients:
            for field in data_fields:
                if getattr(patient, field) is None:
                    continue
                elif getattr(patient, field) not in ('TRUE', 'Positive'):
                    setattr(patient, field, 0)
                else:
                    setattr(patient, field, 1)

    def __build_analysis_vectors(self):
        vector_builder = Analysis_Vector_Builder(data_object_list=self.__patients,
                                                 data_fields=Data_Fields.get_all_data_fields())

        self.__vectors = vector_builder.analysis_vectors

    def __remove_data_fields_with_to_much_missing_data(self):
        for analysis_vector in self.__vectors:
            data_field_name = analysis_vector.field_name
            all_data_points_count = analysis_vector.get_vector_size
            missing_values_count = analysis_vector.get_missing_values_count
            missing_value_ratio = missing_values_count / all_data_points_count

            if missing_value_ratio > Config.DATA_FIELD_MISSING_VALUES_THRESHOLD:
                Config.DATA_FIELDS_IN_ANALYSIS.remove(data_field_name)

    @property
    def get_patients(self):
        return self.__patients

    @property
    def get_vectors(self):
        return self.__vectors
