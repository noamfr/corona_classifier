from typing import List, Dict

from classify.baseline_prediction import Baseline_prediction
from data.data import Data


class Classifier:
    def __init__(self, data: Data):
        self.__data = data
        self.__models: Dict = {}
        self.__baseline_prediction: Baseline_prediction or None

        self.__calc()

    def __calc(self):
        self.__calc_base_line_prediction()

    def __calc_base_line_prediction(self):
        self.__baseline_prediction = Baseline_prediction(X=self.__data.X_train,
                                                         y=self.__data.y_train)

    def __evaluate_training_set_models(self):
        pass

    def __classify_test_set(self):
        pass

    @property
    def tables(self):
        return {Table_Names.CROSS_VAL_SCORES: self.__baseline_prediction.get_cross_val_scores,
                Table_Names.CONFUSION_MATRICES: self.__baseline_prediction.get_confusion_matrices}


class Table_Names:
    CROSS_VAL_SCORES = 'cross_val_scores'
    CONFUSION_MATRICES = 'confusion_matrices'

