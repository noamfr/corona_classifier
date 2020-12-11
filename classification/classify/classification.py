import numpy as np
from collections import defaultdict
from typing import Dict, List

from configuration.classification_config import Classification_Config as Config
from data.data import Data
from .classifiers import Classifiers
from .model_assesment import Model_Assessment


class Classification:
    def __init__(self, data: Data):
        self.__data = data
        self.__X_train: np.ndarray = data.X_train
        self.__y_train: np.ndarray = data.y_train
        self.__X_test: np.ndarray = data.X_test
        self.__y_test: np.ndarray = data.y_test

        self.__classifiers: Dict = {}
        self.__y_pred_probas: Dict[str, np.ndarray] = {}
        self.model_performance_for_thresholds: Dict[str, List] = {}

        self.__calc()

    def __calc(self):
        self.__get_classifiers()
        self.__fit_training_set()
        self.__predict_proba()
        self.__calc_model_performance_for_thresholds()

    def __get_classifiers(self):
        self.__classifiers = Classifiers().get_classifiers()

    def __fit_training_set(self):
        for name, model in self.__classifiers.items():
            model.fit(self.__X_train, self.__y_train)

    def __predict_proba(self):
        y_preds = {}

        for name, model in self.__classifiers.items():
            preds = model.predict_proba(self.__X_train)
            preds_covid_positive = np.array([pred[1] for pred in preds])
            y_preds[name] = preds_covid_positive

        self.__y_pred_probas = y_preds

    def __calc_model_performance_for_thresholds(self):
        model_performance = defaultdict(list)
        y_true = self.__y_train

        for model_name, y_pred_proba in self.__y_pred_probas.items():
            for threshold in Config.MODEL_THRESHOLDS:
                y_pred = self.__calc_y_pred_with_threshold(y_pred_proba, threshold)
                model_assessment = Model_Assessment(y_true=y_true, y_pred=y_pred)

                model_performance[Fields.MODEL_NAME].append(model_name)
                model_performance[Fields.THRESHOLD].append(threshold)

                model_performance[Fields.TRUE_POSITIVE].append(model_assessment.true_positive)
                model_performance[Fields.FALSE_POSITIVE].append(model_assessment.false_positive)
                model_performance[Fields.TRUE_NEGATIVE].append(model_assessment.true_negative)
                model_performance[Fields.FALSE_NEGATIVE].append(model_assessment.false_negative)

                model_performance[Fields.RECALL].append(model_assessment.recall)
                model_performance[Fields.PRECISION].append(model_assessment.precision)
                model_performance[Fields.ACCURACY].append(model_assessment.accuracy)

        self.model_performance_for_thresholds = dict(model_performance)

    @staticmethod
    def __calc_y_pred_with_threshold(y_pred_proba: np.ndarray, threshold: float):
        y_pred_proba = y_pred_proba
        y_preds = []

        for idx in range(len(y_pred_proba)):
            covid_positive_probability = y_pred_proba[idx]
            if covid_positive_probability > threshold:
                y_pred = 1

            else:
                y_pred = 0

            y_preds.append(y_pred)

        return np.array(y_preds)


class Fields:
    MODEL_NAME = 'model name'
    THRESHOLD = 'threshold'

    TRUE_POSITIVE = 'true positive'
    FALSE_POSITIVE = 'false positive'
    TRUE_NEGATIVE = 'true negative'
    FALSE_NEGATIVE = 'false negative'

    RECALL = 'recall'
    PRECISION = 'precision'
    ACCURACY = 'accuracy'

    FIELD_ORDER = [
        MODEL_NAME,
        THRESHOLD,

        RECALL,
        PRECISION,
        ACCURACY,

        TRUE_POSITIVE,
        FALSE_POSITIVE,
        TRUE_NEGATIVE,
        FALSE_NEGATIVE]
