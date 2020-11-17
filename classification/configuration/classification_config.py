import os
import yaml
from typing import List

from data_classes.data_fields import Data_Fields


class Classification_Config:
    WORK_DIR: str
    RAW_DATA_PATH: str
    PICKLE_PATH: str
    YAML_FILE_PATH: str
    DATA_FIELDS_IN_ANALYSIS: List

    DATA_FIELD_MISSING_VALUES_THRESHOLD: float
    BOOTSTRAP_PATIENT_ENLARGEMENT_SIZE: float

    def __init__(self):
        self.__class__.WORK_DIR = 'C:/Users/normy/corona_classifier_files/classification'
        self.__class__.RAW_DATA_PATH = 'C:/Users/normy/PycharmProjects/covidclinicaldata/data'
        self.__class__.PICKLE_PATH = os.path.join(self.WORK_DIR, 'pickle_files')
        self.__class__.YAML_FILE_PATH = os.path.join(os.path.dirname(__file__), 'yaml_files')
        self.__class__DATA_FIELDS_IN_ANALYSIS = [Data_Fields.get_target()] + Data_Fields.get_binary_vars()

        static_values = self.load_yaml(file_name='static_values')
        self.__class__.DATA_FIELD_MISSING_VALUES_THRESHOLD = static_values['data_field_missing_values_threshold']
        self.__class__.BOOTSTRAP_PATIENT_ENLARGEMENT_SIZE = static_values['bootstrap_patient_enlargement_size']

    @classmethod
    def remove_data_field_from_analysis(cls, data_field: str):
        cls.DATA_FIELDS_IN_ANALYSIS.remove(data_field)

    @classmethod
    def load_yaml(cls, file_name):
        with open(os.path.join(cls.YAML_FILE_PATH, f'{file_name}.yaml'), 'r') as data:
            data_loaded = yaml.safe_load(data)
        return data_loaded
