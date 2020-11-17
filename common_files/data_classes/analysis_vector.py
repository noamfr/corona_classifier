import numpy as np
from typing import List


class Analysis_Vector:
    def __init__(self, field_name: str, vector: np.ndarray, missing_values_idx: List):
        self.__field_name = field_name
        self.__vector = vector
        self.__missing_values_idx = missing_values_idx

    @property
    def field_name(self):
        return self.__field_name

    @property
    def vector(self):
        return self.__vector

    @property
    def vector_without_missing_values(self):
        vector_without_missing_values = np.delete(self.__vector, self.__missing_values_idx)
        return vector_without_missing_values

    @property
    def missing_values_idx(self):
        return self.__missing_values_idx

    @property
    def get_missing_values_count(self):
        return len(self.__missing_values_idx)

    @property
    def get_vector_size(self):
        return len(self.__vector)

    @classmethod
    def get_same_length_vectors(cls, vector_list: List):
        same_length_vectors = {}
        aggregated_missing_idx = cls.get_aggregated_missing_idx(vector_list=vector_list)

        for analysis_vector in vector_list:
            same_length_vector = np.delete(analysis_vector.vector, aggregated_missing_idx)
            same_length_vectors[analysis_vector.field_name] = same_length_vector
        return same_length_vectors

    @classmethod
    def get_aggregated_missing_idx(cls, vector_list: List):
        aggregated_missing_idx = set()
        for vector in vector_list:
            aggregated_missing_idx.update(vector.missing_values_idx)

        return aggregated_missing_idx


class Analysis_Vector_Builder:
    def __init__(self, data_object_list: List, data_fields: List[str]):
        self.__data_object_list = data_object_list
        self.__data_fields = data_fields
        self.__analysis_vectors: List = []

        self.__build_analysis_vectors()

    def __build_analysis_vectors(self):
        vectors = []

        for data_field in self.__data_fields:
            vector = np.array([getattr(data_object, data_field) for data_object in self.__data_object_list])

            missing_values_idx = [idx for idx, value in enumerate(vector) if value in (None, np.nan)]

            analysis_vector = Analysis_Vector(field_name=data_field,
                                              vector=vector,
                                              missing_values_idx=missing_values_idx)

            vectors.append(analysis_vector)

        self.__analysis_vectors = vectors

    def __get_aggregated_missing_idx(self):
        aggregated_missing_idx = set()
        for data_field in self.__analysis_vectors:
            missing_values_idx = self.__analysis_vectors[data_field].__missing_values_idx()

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


class Vector_Groups:
    TARGET = 'target'
    BINARY_VECTORS = 'binary_vectors'
    CONTINUOUS_VECTORS = 'continuous_vectors'


def get_same_length_vectors(vector_list: List[Analysis_Vector]):
    same_length_vectors = {}
    aggregated_missing_idx = get_aggregated_missing_idx(vector_list=vector_list)

    for analysis_vector in vector_list:
        same_length_vector = np.delete(analysis_vector.vector, aggregated_missing_idx)
        same_length_vectors[analysis_vector.field_name] = same_length_vector
    return same_length_vectors


def get_aggregated_missing_idx(vector_list: List[Analysis_Vector]):
    aggregated_missing_idx = set()
    for vector in vector_list:
        aggregated_missing_idx.update(vector.missing_values_idx)

    return aggregated_missing_idx
