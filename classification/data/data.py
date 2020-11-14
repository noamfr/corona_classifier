from typing import List

from data_analysis.data.patient import Patient
from data_analysis.data.data_fields import Data_Fields
from data_analysis.data.vector_builder import Vector_Builder, Analysis_Vector

from configuration.classification_config import Classification_Config


class Data:
    def __init__(self, patients: List[Patient]):
        self.__patients = patients
        self.__vectors: List[Analysis_Vector] = []

    def __calc(self):
        self.__binary_one_hot_encoding()
        self.__build_analysis_vectors()
        # self.__remove_data_fields_with_to_much_missing_data()

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
        vector_builder = Vector_Builder(data_object_list=self.__patients,
                                        data_fields=Data_Fields.get_all_data_fields())

        self.__vectors = vector_builder.analysis_vectors

    def __remove_data_fields_with_to_much_missing_data(self):
        for analysis_vector in self.__vectors:
            data_field_name = analysis_vector.field_name
            all_data_points_count = analysis_vector.get_vector_size
            missing_values_count = analysis_vector.get_missing_values_count
            missing_value_ratio = missing_values_count / all_data_points_count

            if missing_value_ratio > Classification_Config.DATA_FIELD_MISSING_VALUES_THRESHOLD:
                Classification_Config.DATA_FIELDS_IN_ANALYSIS.remove(data_field_name)

    @property
    def get_patients(self):
        return self.__patients

    @property
    def get_vectors(self):
        return self.__vectors
