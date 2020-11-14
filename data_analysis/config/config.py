import os
import yaml
from typing import Set, Dict

from data.data_fields import Data_Fields


class Config:
    WORK_DIR: str
    RAW_DATA_PATH: str
    YAML_FILE_PATH: str
    PICKLE_PATH: str
    DATA_ANALYSIS_OUTPUTS_PATH: str

    DATA_FIELDS_IN_ANALYSIS: Set[str]

    DATA_FIELD_MISSING_VALUES_THRESHOLD: float
    BOOTSTRAP_ITERATIONS: int
    ADULT_AGE_THRESHOLD: int

    CONTINUOUS_FIELDS_NORMAL_VALUES: Dict

    def __init__(self):

        __class__.WORK_DIR = 'C:/Users/normy/corona_classifier_files'
        __class__.RAW_DATA_PATH = 'C:/Users/normy/PycharmProjects/covidclinicaldata/data'
        __class__.YAML_FILE_PATH = os.path.join(os.path.dirname(__file__), 'yaml_files')
        __class__.PICKLE_PATH = os.path.join(Config.WORK_DIR, 'pickle_files')
        __class__.DATA_ANALYSIS_OUTPUTS_PATH = os.path.join(Config.WORK_DIR, 'data_analysis_outputs')
        __class__.DATA_FIELDS_IN_ANALYSIS = set(Data_Fields.get_all_data_fields())

        static_values = self.load_yaml(file_name='static_values')
        __class__.DATA_FIELD_MISSING_VALUES_THRESHOLD = static_values['data_field_missing_values_threshold']
        __class__.BOOTSTRAP_ITERATIONS = static_values['bootstrap_iterations']
        __class__.ADULT_AGE_THRESHOLD = static_values['adult_age_threshold']

        __class__.CONTINUOUS_FIELDS_NORMAL_VALUES = self.load_yaml(file_name='continuous_fields_healthy_values')

    @classmethod
    def remove_data_field_from_analysis(cls, data_field: str):
        cls.DATA_FIELDS_IN_ANALYSIS.remove(data_field)

    @staticmethod
    def load_yaml(file_name):
        with open(os.path.join(Config.YAML_FILE_PATH, f'{file_name}.yaml'), 'r') as data:
            data_loaded = yaml.safe_load(data)
        return data_loaded
