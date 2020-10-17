from os import path, listdir
import yaml
from typing import Dict

from .static_values import Static_Configs
from .vitals_values import Vital_Values, Vitals_Container


class Config:
    WORK_DIR: str
    RAW_DATA_PATH: str
    PICKLE_PATH: str
    DATA_ANALYSIS_OUTPUTS_PATH: str
    ADULT_AGE_THRESHOLD: int
    YAML_FILE_PATH: str
    ACCEPTED_VALUES_YAML_PATH: str
    ANALYSIS_TABLE_NAMES: Dict
    CHILDREN_HEALTHY_LOWER: Dict
    CHILDREN_HEALTHY_UPPER: Dict
    VITALS_CONTAINER: Vitals_Container

    def __init__(self):

        __class__.WORK_DIR = 'C:/Users/normy/corona_classifier_files'
        __class__.RAW_DATA_PATH = 'C:/Users/normy/PycharmProjects/covidclinicaldata/data'
        __class__.PICKLE_PATH = path.join(Config.WORK_DIR, 'pickle_files')
        __class__.DATA_ANALYSIS_OUTPUTS_PATH = path.join(Config.WORK_DIR, 'data_analysis_outputs')
        __class__.ADULT_AGE_THRESHOLD = Static_Configs.ADULT_AGE_THRESHOLD
        __class__.YAML_FILE_PATH = 'config/yaml_files'

        __class__.ACCEPTED_VALUES_YAML_PATH = 'config/accepted_values_yamls'
        __class__.ANALYSIS_TABLE_NAMES = self.load_yaml('analysis_table_names')

    @classmethod
    def get_missing_value_threshold(cls):
        return Static_Configs.MISSING_VALUES_THRESHOLD

    @staticmethod
    def load_yaml(file_name):
        with open(path.join(Config.YAML_FILE_PATH, f'{file_name}.yaml'), 'r') as data:
            data_loaded = yaml.safe_load(data)
        return data_loaded

    def load_vitals(self, file_name):
        vitals = self.load_yaml(file_name)
        vital_values = Vital_Values(population=vitals['population'],
                                    threshold_category=vitals['threshold_category'],
                                    threshold_type=vitals['threshold_type'],
                                    temperature=vitals['temperature'],
                                    pulse=vitals['pulse'],
                                    sys=vitals['sys'],
                                    dia=vitals['dia'],
                                    rr=vitals['rr'],
                                    sats=vitals['sats'])

        return vital_values

    def build_vitals_container(self):
        vitals_container = Vitals_Container()
        for file_name in listdir(Config.ACCEPTED_VALUES_YAML_PATH):
            vitals = self.load_vitals(file_name)
            setattr(vitals_container, file_name, vitals)
            vitals_container.vitals_list.append(vitals)

        return vitals_container







    # def __load__vitals_thresholds_from_yaml(self, population, threshold_category, threshold_type):
    #     vitals_threshold_map = defaultdict[lambda: defaultdict(dict)]
    #     for file_name in listdir(path.join(Config.ACCEPTED_VALUES_YAML_PATH,
    #                                        population, threshold_category, threshold_type)):
    #
    #         vitals = self.load_yaml(file_name)
    #         vitals_threshold_map[population][threshold_category][threshold_type] = vitals
    #
    #     #
    #     # for population in [Population.CHILDREN, Population.ADULTS]:
    #     #     for threshold_category in [Threshold_Category.HEALTHY_VALUES, Threshold_Category.ACCEPTED_VALUES]:
    #     #         for threshold_type in [Threshold_Type.LOWER, Threshold_Type.UPPER]:
    #     #             for file_name in listdir(path.join(Config.ACCEPTED_VALUES_YAML_PATH, population)):
    #     #                 vitals = self.load_yaml(file_name)
        #                 if population == Population.CHILDREN:
        #                     __class__.CHILDREN_VITALS = {}
        #                     __class__.CHILDREN_VITALS['lower] = Accepted_Value_Map(temperature=vitals['temperature'],
        #                                                                    pulse=vitals['pulse'],
        #                                                                    sys=vitals['sys'],
        #                                                                    dia=vitals['dia'],
        #                                                                    rr=vitals['rr'],
        #                                                                    sats=vitals['sats'])
        #
        #





