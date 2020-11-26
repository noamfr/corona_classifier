import os
import pandas as pd
from typing import Dict

from classify.classifier import Classifier, Table_Names
from configuration.classification_config import Classification_Config as Config


class Publisher:
    def __init__(self, classifier: Classifier):
        self.__tables: Dict = classifier.tables

        self.__publish()

    def __publish(self):
        self.__publish_cross_val_scores()
        self.__publish_confusion_matrices()

    def __publish_cross_val_scores(self):
        cross_val_scores_df = pd.DataFrame(self.__tables[Table_Names.CROSS_VAL_SCORES])
        cross_val_scores_df.to_csv(os.path.join(Config.OUTPUT_PATH, 'baseline_cross_val_scores.csv'))

    def __publish_confusion_matrices(self):
        for name, matrix in self.__tables[Table_Names.CONFUSION_MATRICES].items():
            table_df = pd.DataFrame(matrix)
            table_df.to_csv(os.path.join(Config.OUTPUT_PATH, f'confusion_matrix_{name}.csv'))
