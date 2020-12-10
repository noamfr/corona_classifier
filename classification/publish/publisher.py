import os
import pandas as pd
from typing import Dict

from classify.classification import Classification, Fields
from configuration.classification_config import Classification_Config as Config


class Publisher:
    def __init__(self, classification: Classification):
        self.__model_performance_for_thresholds: Dict = classification.model_performance_for_thresholds

        self.__publish()

    def __publish(self):
        self.__publish_model_performance_for_thresholds()

    def __publish_model_performance_for_thresholds(self):
        df = pd.DataFrame(self.__model_performance_for_thresholds, columns=Fields.FIELD_ORDER)
        df.to_csv(os.path.join(Config.OUTPUT_PATH, '__model_performance_for_thresholds.csv'))
