import os
import numpy as np
from collections import defaultdict
from typing import List

from corona_data_analysis.data.data_fields import Data_Fields
from corona_data_analysis.config.config import Config


class Prep_Data:
    def __init__(self, patients):
        self.patients = patients
        self.local_output_path = os.path.join(Config.OUTPUT_PATH, 'data_prep')

    def prep_data(self):
        self.__one_hot_encoding()
        # self.__continuous_vars_quality_analysis()

    def __get_binary_values(self):
        binary_data_fields = Data_Fields.get_binary_vars()
        binary_vars_unique = defaultdict(set)
        for patient in self.patients:
            for field in binary_data_fields:
                value = getattr(patient, field)
                binary_vars_unique[field].add(value)

        return binary_vars_unique

    def __one_hot_encoding(self):
        binary_data_fields = Data_Fields.get_binary_vars()

        for patient in self.patients:
            for field in binary_data_fields:
                if getattr(patient, field) is None:
                    continue

                if getattr(patient, field) not in ('TRUE', 'Positive'):
                    setattr(patient, field, 0)

                else:
                    setattr(patient, field, 1)



    def __continuous_vars_quality_analysis(self):
        continuous_fields = Data_Fields.get_continuous_vars()
        continuous_fields.remove(Data_Fields.AGE.field_name)

        age_vec = self.__build_vector_from_object_list(object_field=Data_Fields.AGE.field_name, object_list=self.patients,
                                                       remove_missing_values=False)
        for field in continuous_fields:
            vec = self.__build_vector_from_object_list(object_field=field, object_list=self.patients,
                                                       remove_missing_values=True)

    # def calc_values_in_threshold_count(self, vector: np.ndarray, vital_name: str, ):
    #     adult_lower_threshold = Config.VITALS_CONTAINER.get_vital(Population.ADULTS,
    #                                                                       Threshold_Category.HEALTHY,
    #                                                                       Threshold_Type.LOWER,
    #                                                                       getattr(Vitals_Names, vital_name))
    #
    #     adult_upper_threshold = Config.VITALS_CONTAINER.get_vital(Population.ADULTS,
    #                                                                       Threshold_Category.HEALTHY,
    #                                                                       Threshold_Type.UPPER,
    #                                                                       getattr(Vitals_Names, vital_name))



    def __build_vector_from_object_list(self, object_list: List, object_field: str, remove_missing_values: bool):
        vector = np.array([getattr(object_instance, object_field) for object_instance in object_list])

        if remove_missing_values:
            vector = self.__remove_missing_values_from_vector(vector)

        return vector

    @staticmethod
    def __remove_missing_values_from_vector(vector: np.ndarray):

        idx = 0
        idx_to_remove = []
        for value in vector:
            if value in [None, np.nan]:
                idx_to_remove.append(idx)

        vector = np.delete(vector, idx_to_remove)

        return vector
