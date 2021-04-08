import os
import yaml
from typing import List, Dict

from data_classes.data_fields import Data_Fields


class Classification_Config:
    WORK_DIR: str
    COMMON_FILES_DIR: str
    RAW_DATA_PATH: str
    PICKLE_PATH: str
    YAML_FILE_DIR: str
    COMMON_YAML_FILE_DIR: str
    OUTPUT_PATH: str
    DATA_FIELDS_IN_ANALYSIS: List

    DATA_FIELD_MISSING_VALUES_THRESHOLD: float
    PATIENT_MISSING_VALUES_THRESHOLD: int
    BOOTSTRAP_PATIENT_ENLARGEMENT_SIZE: float
    MODEL_THRESHOLDS: List[float]

    CONTINUOUS_FIELDS_THRESHOLDS: Dict[str, Dict[str, Dict[str, int]]]
    XGB_BASE_MODEL_VALUES: Dict[str, float or int]

    def __init__(self):
        self.__class__.WORK_DIR = 'C:/Users/normy/corona_classifier_files/classification'
        self.__class__.COMMON_FILES_DIR = 'C:/Users/normy/PycharmProjects/corona_classifier/common_files'
        self.__class__.RAW_DATA_PATH = os.environ['RAW_DATA_PATH']
        self.__class__.PICKLE_PATH = os.path.join(self.WORK_DIR, 'pickle_files')
        self.__class__.YAML_FILE_DIR = os.path.join(os.path.dirname(__file__), 'yaml_files')
        self.__class__.COMMON_YAML_FILE_DIR = os.path.join(self.COMMON_FILES_DIR, 'yaml_files')
        self.__class__.OUTPUT_PATH = os.path.join(self.WORK_DIR, 'outputs')

        self.__class__.DATA_FIELDS_IN_ANALYSIS = [Data_Fields.get_target(),
                                                  *Data_Fields.get_binary_vars(),
                                                  *Data_Fields.get_continuous_vars()]

        static_values = self.load_yaml(self.YAML_FILE_DIR, 'static_values')
        self.__class__.DATA_FIELD_MISSING_VALUES_THRESHOLD = static_values['data_field_missing_values_threshold']
        self.__class__.PATIENT_MISSING_VALUES_THRESHOLD = static_values['patient_missing_values_threshold']
        self.__class__.BOOTSTRAP_PATIENT_ENLARGEMENT_SIZE = static_values['bootstrap_patient_enlargement_size']
        self.__class__.MODEL_THRESHOLDS = static_values['model_thresholds']

        self.__class__.CONTINUOUS_FIELDS_THRESHOLDS = self.load_yaml(self.COMMON_YAML_FILE_DIR, 'continuous_fields_thresholds')

        self.__class__.XGB_BASE_MODEL_VALUES = self.load_yaml(self.YAML_FILE_DIR, 'xgb_base_model_values')


    @classmethod
    def remove_data_field_from_analysis(cls, data_field: str):
        cls.DATA_FIELDS_IN_ANALYSIS.remove(data_field)

    @classmethod
    def load_yaml(cls, path: str, file_name: str):
        with open(os.path.join(path, f'{file_name}.yaml'), 'r') as data:
            data_loaded = yaml.safe_load(data)
        return data_loaded

    @classmethod
    def load_common_yaml(cls, file_name):
        with open(os.path.join(cls.COMMON_FILES_DIR, 'yaml_files', f'{file_name}.yaml'), 'r') as data:
            data_loaded = yaml.safe_load(data)
        return data_loaded

    @classmethod
    def get_continuous_field_threshold(cls, age_group: str, threshold: str, vital_value_name: str):
        return cls.CONTINUOUS_FIELDS_THRESHOLDS[age_group][threshold][vital_value_name]
