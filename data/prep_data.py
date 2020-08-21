from collections import defaultdict
from get_data.data_fields import Data_Fields


class Prep_Data:
    def __init__(self, patients):
        self.patients = patients

    def prep_data(self):
        self.__one_hot_encoding()

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
