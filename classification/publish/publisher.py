import pandas as pd
from typing import Dict

from data_operations.df_printer import save_df_as_table

from classify.classification import Classification
from classify.table_fields import Model_Performance_Fields, Feature_Importance_Fields
from configuration.classification_config import Classification_Config as Config


class Publisher:
    def __init__(self, classification: Classification):
        self.__model_performance_for_thresholds: Dict = classification.model_performance_for_thresholds
        self.__feature_importance = classification.feature_importance

        self.__publish()

    def __publish(self):
        self.__publish_model_performance_for_thresholds()
        self.__publish_feature_importance()

    def __publish_model_performance_for_thresholds(self):
        df = pd.DataFrame(self.__model_performance_for_thresholds)

        save_df_as_table(df=df,
                         column_order=Model_Performance_Fields.FIELD_ORDER,
                         path=Config.OUTPUT_PATH,
                         file_name='model_performance_for_thresholds.csv')

    def __publish_feature_importance(self):
        df = pd.DataFrame(self.__feature_importance)
        df.sort_values(by='gain', ascending=False, inplace=True)

        save_df_as_table(df=df,
                         column_order=['predictor name', 'gain', 'weight', 'cover', 'total_gain', 'total_cover'],
                         path=Config.OUTPUT_PATH,
                         file_name='Feature_Importance.csv')
