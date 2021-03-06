import numpy as np
from sklearn.model_selection import train_test_split
from typing import List, Dict

from data_classes.patient import Patient
from data_classes.data_fields import Data_Fields
from data_classes.analysis_vector import Analysis_Vector_Builder, Analysis_Vector

from configuration.classification_config import Classification_Config as Config


class Data:
    def __init__(self, patients: List[Patient]):
        self.__patients = patients
        self.__vectors: List[Analysis_Vector] = []
        self.__same_length_vectors: Dict[str, np.ndarray] = {}
        self.__training_set: Dict[str, np.ndarray] = {}
        self.__test_set: Dict[str, np.ndarray] = {}

        self.predictors_names: List[str] = []
        self.X_train: np.ndarray or None = None
        self.X_val: np.ndarray or None = None
        self.X_test: np.ndarray or None = None

        self.y_train: np.ndarray or None = None
        self.y_val: np.ndarray or None = None
        self.y_test: np.ndarray or None = None

        self.__calc()

    def __calc(self):
        self.__replace_empty_strings_with_none()
        self.__binary_one_hot_encoding()
        self.__remove_data_fields_with_to_much_missing_data()
        self.__remove_patients_with_to_much_missing_values()
        self.__replace_un_accepted_vital_values_with_none()
        self.__bootstrap_enlargement_of_target_positive_patients()
        self.__calc_analysis_vectors()
        self.__get_same_length_vectors()
        self.__normalize_continuous_vectors()
        self.__standardize_continuous_vectors()
        self.__train_test_val_split()

    def __replace_empty_strings_with_none(self):
        data_fields = Data_Fields.get_all_data_fields()
        for patient in self.__patients:
            for data_field in data_fields:
                if getattr(patient, data_field) == '':
                    setattr(patient, data_field, None)

    def __binary_one_hot_encoding(self):
        binary_data_fields = [Data_Fields.get_target()] + Data_Fields.get_binary_vars()

        for patient in self.__patients:
            for field in binary_data_fields:
                if getattr(patient, field) is None:
                    continue

                elif getattr(patient, field) not in ('TRUE', 'Positive'):
                    setattr(patient, field, 0)

                else:
                    setattr(patient, field, 1)

    def __remove_data_fields_with_to_much_missing_data(self):
        for data_field in Data_Fields.get_all_data_fields():
            missing_data_count = 0
            for patient in self.__patients:
                if getattr(patient, data_field) is None:
                    missing_data_count += 1

            missing_data_ratio = missing_data_count / len(self.__patients)
            if missing_data_ratio >= Config.DATA_FIELD_MISSING_VALUES_THRESHOLD:
                if data_field in Config.DATA_FIELDS_IN_ANALYSIS:
                    Config.DATA_FIELDS_IN_ANALYSIS.remove(data_field)

    def __remove_patients_with_to_much_missing_values(self):
        idx_to_remove = set()
        for idx in range(len(self.__patients)):
            missing_values_count = 0

            for data_field in Config.DATA_FIELDS_IN_ANALYSIS:
                if getattr(self.__patients[idx], data_field) is None:
                    missing_values_count += 1

            if missing_values_count > Config.PATIENT_MISSING_VALUES_THRESHOLD:
                idx_to_remove.add(idx)

        idx_to_remove = sorted(idx_to_remove, reverse=True)
        for idx in idx_to_remove:
            self.__patients.pop(idx)

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

            for field_name in Data_Fields.get_continuous_vars():
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


    def __bootstrap_enlargement_of_target_positive_patients(self):
        target_positive_patients_idx = self.__get_target_positive_patients_idx(patients=self.__patients)
        bootstrap_size = Config.BOOTSTRAP_PATIENT_ENLARGEMENT_SIZE

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

    def __calc_analysis_vectors(self):
        vector_builder = Analysis_Vector_Builder(data_object_list=self.__patients,
                                                 data_fields=Config.DATA_FIELDS_IN_ANALYSIS)

        self.__vectors = vector_builder.analysis_vectors

    def __get_same_length_vectors(self):
        same_length_vectors = Analysis_Vector.get_same_length_vectors(vector_list=self.__vectors)
        self.__same_length_vectors = same_length_vectors

    def __normalize_continuous_vectors(self):
        for field_name in Data_Fields.get_continuous_vars():
            if field_name in Config.DATA_FIELDS_IN_ANALYSIS:
                normalized_values = []
                vector = self.__same_length_vectors[field_name]
                min_value = vector.min()
                max_value = vector.max()

                for value in vector:
                    new_value = (value - min_value) / (max_value - min_value)
                    normalized_values.append(new_value)

                self.__same_length_vectors[field_name] = np.array(normalized_values)

    def __standardize_continuous_vectors(self):
        for field_name in Data_Fields.get_continuous_vars():
            if field_name in Config.DATA_FIELDS_IN_ANALYSIS:
                standardized_values = []
                vector = self.__same_length_vectors[field_name]
                mean_value = vector.mean()
                std_value = vector.std()

                for value in vector:
                    new_value = (value - mean_value) / std_value
                    standardized_values.append(new_value)

                self.__same_length_vectors[field_name] = np.array(standardized_values)


    def __train_test_val_split(self):
        y = self.__same_length_vectors[Data_Fields.get_target()]
        binary_fields = [field for field in Data_Fields.get_binary_vars() if field in Config.DATA_FIELDS_IN_ANALYSIS]
        continuous_fields = [field for field in Data_Fields.get_continuous_vars() if field in Config.DATA_FIELDS_IN_ANALYSIS]
        predictors_names = binary_fields + continuous_fields

        predictors_vectors_tuple = tuple([self.__same_length_vectors[name] for name in predictors_names])
        X = np.stack(predictors_vectors_tuple, axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)


        self.X_train = X_train
        self.X_val = X_val
        self.X_test = X_test
        self.y_train = y_train
        self.y_val = y_val
        self.y_test = y_test
        self.predictors_names = predictors_names

    @property
    def get_predictors_names(self):
        return self.predictors_names

    @property
    def get_vectors(self):
        return self.__vectors
