import os
import yaml
from typing import Set, Dict, List

from data_classes.data_fields import Data_Fields


class Data_Analysis_Config:
    WORK_DIR: str
    COMMON_FILE_PATH: str
    RAW_DATA_PATH: str
    LOCAL_YAML_FILE_PATH: str
    COMMON_YAML_FILE_PATH: str
    PICKLE_PATH: str
    DATA_ANALYSIS_OUTPUTS_PATH: str

    DATA_FIELDS_IN_ANALYSIS: Set[str]

    DATA_FIELD_MISSING_VALUES_THRESHOLD: float
    BOOTSTRAP_ITERATIONS: int


    CONTINUOUS_FIELDS_THRESHOLDS: Dict[str, Dict[str, Dict]]


    def __init__(self):

        self.__class__.WORK_DIR = 'C:/Users/normy/corona_classifier_files'
        self.__class__.COMMON_FILE_PATH = 'C:/Users/normy/PycharmProjects/corona_classifier/common_files'
        self.__class__.RAW_DATA_PATH = 'C:/Users/normy/PycharmProjects/covidclinicaldata/data'
        self.__class__.LOCAL_YAML_FILE_PATH = os.path.join(os.path.dirname(__file__), 'yaml_files')
        self.__class__.COMMON_YAML_FILE_PATH = os.path.join(Data_Analysis_Config.COMMON_FILE_PATH, 'yaml_files')
        self.__class__.PICKLE_PATH = os.path.join(Data_Analysis_Config.WORK_DIR, 'pickle_files')
        self.__class__.DATA_ANALYSIS_OUTPUTS_PATH = os.path.join(Data_Analysis_Config.WORK_DIR, 'data_analysis_outputs')
        self.__class__.DATA_FIELDS_IN_ANALYSIS = set(Data_Fields.get_all_data_fields())

        static_values = self.load_local_yaml(file_name='static_values')
        self.__class__.DATA_FIELD_MISSING_VALUES_THRESHOLD = static_values['data_field_missing_values_threshold']
        self.__class__.BOOTSTRAP_ITERATIONS = static_values['bootstrap_iterations']

        self.__class__.CONTINUOUS_FIELDS_THRESHOLDS = self.load_common_yaml(file_name='continuous_fields_thresholds')


    @classmethod
    def remove_data_field_from_analysis(cls, data_field: str):
        cls.DATA_FIELDS_IN_ANALYSIS.remove(data_field)

    @staticmethod
    def load_local_yaml(file_name):
        with open(os.path.join(Data_Analysis_Config.LOCAL_YAML_FILE_PATH, f'{file_name}.yaml'), 'r') as data:
            data_loaded = yaml.safe_load(data)
        return data_loaded

    @staticmethod
    def load_common_yaml(file_name):
        with open(os.path.join(Data_Analysis_Config.COMMON_YAML_FILE_PATH, f'{file_name}.yaml'), 'r') as data:
            data_loaded = yaml.safe_load(data)
        return data_loaded

    @classmethod
    def get_continuous_field_threshold(cls, age_group: str, threshold: str, vital_value_name: str):
        return cls.CONTINUOUS_FIELDS_THRESHOLDS[age_group][threshold][vital_value_name]

