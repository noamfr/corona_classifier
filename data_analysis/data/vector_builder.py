import numpy as np
from typing import List, Dict


class Analysis_Vector:
    def __init__(self, field_name: str, vector: np.ndarray, missing_values_idx: List):
        self.field_name = field_name
        self.vector = vector
        self.missing_values_idx = missing_values_idx


class Vector_Builder:
    def __init__(self, data_object_list: List, data_fields: List[str], array_type=float):
        self.__data_object_list = data_object_list
        self.__data_fields = data_fields
        self.__array_type = array_type
        self.__analysis_vectors: Dict[str: Analysis_Vector] = {}

        self.__build_analysis_vectors()

    def __build_analysis_vectors(self):
        vectors = {}

        for data_field in self.__data_fields:
            vector = np.array([getattr(data_object, data_field) for data_object in self.__data_object_list])
            vector = vector.astype(self.__array_type)

            missing_values_idx = [idx for idx, value in enumerate(vector) if value in (None, np.nan)]

            analysis_vector = Analysis_Vector(field_name=data_field,
                                              vector=vector,
                                              missing_values_idx=missing_values_idx)

            vectors[data_field] = analysis_vector

        self.vectors = vectors

    def __get_aggregated_missing_idx(self):
        aggregated_missing_idx = set()
        for data_field in self.__analysis_vectors:
            missing_values_idx = self.__analysis_vectors[data_field].missing_values_idx()

            aggregated_missing_idx.update(missing_values_idx)

        return list(aggregated_missing_idx)

    def __get_same_length_vectors(self):
        aggregated_missing_idx = self.__get_aggregated_missing_idx()
        same_length_vectors = {}

        for data_field in self.__analysis_vectors:
            same_length_vector = np.delete(self.__analysis_vectors[data_field], aggregated_missing_idx)
            same_length_vectors[data_field] = same_length_vector

        return same_length_vectors

    @property
    def analysis_vectors(self):
        return self.__analysis_vectors
