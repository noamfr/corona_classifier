import random
import numpy as np
from typing import List, Dict

from data_classes.patient import Patient
from data_classes.data_fields import Data_Fields
from data_classes.analysis_vector import Analysis_Vector_Builder, Analysis_Vector

from configuration.classification_config import Classification_Config


class Data:
    def __init__(self, patients: List[Patient]):
        self.__patients = patients
        self.__vectors: List[Analysis_Vector] = []
        self.__same_length_vectors: Dict[str, np.ndarray] = {}

    def __calc(self):
        self.__binary_one_hot_encoding()
        self.__bootstrap_enlargement_of_target_positive_patients()
        self.__calc_analysis_vectors()
        self.__remove_data_fields_with_to_much_missing_data()
        self.__get_same_length_vectors()
        self.__train_test_split()
        self.__calc_analysis_vectors()
        self.__remove_data_fields_with_to_much_missing_data()

    def __binary_one_hot_encoding(self):
        data_fields = [Data_Fields.get_target()] + Data_Fields.get_binary_vars()

        for patient in self.__patients:
            for field in data_fields:
                if getattr(patient, field) is None:
                    continue

                elif getattr(patient, field) not in ('TRUE', 'Positive'):
                    setattr(patient, field, 0)

                else:
                    setattr(patient, field, 1)

    def __bootstrap_enlargement_of_target_positive_patients(self):
        target_positive_patients_idx = self.__get_target_positive_patients_idx(patients=self.__patients)
        bootstrap_size = Classification_Config.BOOTSTRAP_PATIENT_ENLARGEMENT_SIZE

        idx_to_add = np.random.choice(a=target_positive_patients_idx,
                                      size=round(len(target_positive_patients_idx) * bootstrap_size))

        for idx in idx_to_add:
            self.__patients.append(self.__patients[idx])

    @staticmethod
    def __get_target_positive_patients_idx(patients: List[Patient]):
        target_positive_patients_idx = []

        for idx in range(len(patients)):
            if patients[idx].covid19_test_results == 1:
                target_positive_patients_idx.append(idx)

        return target_positive_patients_idx

    def __remove_data_fields_with_to_much_missing_data(self):
        for analysis_vector in self.__vectors:
            data_field_name = analysis_vector.field_name
            all_data_points_count = analysis_vector.get_vector_size
            missing_values_count = analysis_vector.get_missing_values_count
            missing_value_ratio = missing_values_count / all_data_points_count

            if missing_value_ratio > Classification_Config.DATA_FIELD_MISSING_VALUES_THRESHOLD:
                Classification_Config.DATA_FIELDS_IN_ANALYSIS.remove(data_field_name)

    def __calc_analysis_vectors(self):
        vector_builder = Analysis_Vector_Builder(data_object_list=self.__patients,
                                                 data_fields=Classification_Config.DATA_FIELDS_IN_ANALYSIS)

        self.__vectors = vector_builder.analysis_vectors

    def __get_same_length_vectors(self):
        same_length_vectors = Analysis_Vector.get_same_length_vectors(vector_list=self.__vectors)
        self.__same_length_vectors = same_length_vectors



    def __train_test_split(self):
        random.shuffle(self.__patients)
        corona_positive_patients, corona_negative_patients = self.__split_patients_by_target(self.__patients)





    @staticmethod
    def __split_patients_by_target(patients: [Patient]):
        corona_positive_patients = []
        corona_negative_patients = []

        for patient in patients:
            if patient.covid19_test_results == 1:
                corona_positive_patients.append(patient)
            else:
                corona_negative_patients.append(patient)

        return corona_positive_patients, corona_negative_patients



    @property
    def get_patients(self):
        return self.__patients

    @property
    def get_vectors(self):
        return self.__vectors
