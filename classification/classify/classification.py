import numpy as np
from collections import defaultdict
from typing import Dict, List

from configuration.classification_config import Classification_Config as Config
from data.data import Data
from .classifiers import Classifiers
from .model_assesment import Model_Assessment
from .table_fields import Model_Performance_Fields, Feature_Importance_Fields


class Classification:
    def __init__(self, data: Data):
        self.__data = data
        self.__X_train: np.ndarray = data.X_train
        self.__y_train: np.ndarray = data.y_train
        self.__X_val: np.ndarray = data.X_val
        self.__y_val: np.ndarray = data.y_val

        self.__classifiers: Dict = {}
        self.__y_pred_probas: Dict[str, np.ndarray] = {}

        self.model_performance_for_thresholds: Dict[str, List] = {}
        self.feature_importance: Dict[str, List] = {}

        self.__calc()

    def __calc(self):
        self.__get_classifiers()
        self.__fit_training_set()
        self.__predict_proba()
        self.__calc_model_performance_for_thresholds()
        self.__calc_feature_importance()

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

                model_performance[Model_Performance_Fields.MODEL_NAME].append(model_name)
                model_performance[Model_Performance_Fields.THRESHOLD].append(threshold)

                model_performance[Model_Performance_Fields.TRUE_POSITIVE].append(model_assessment.true_positive)
                model_performance[Model_Performance_Fields.FALSE_POSITIVE].append(model_assessment.false_positive)
                model_performance[Model_Performance_Fields.TRUE_NEGATIVE].append(model_assessment.true_negative)
                model_performance[Model_Performance_Fields.FALSE_NEGATIVE].append(model_assessment.false_negative)

                model_performance[Model_Performance_Fields.RECALL].append(model_assessment.recall)
                model_performance[Model_Performance_Fields.PRECISION].append(model_assessment.precision)
                model_performance[Model_Performance_Fields.F1_SCORE].append(model_assessment.f1_score)
                model_performance[Model_Performance_Fields.ACCURACY].append(model_assessment.accuracy)

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

    def __calc_feature_importance(self):
        predictor_names = self.__data.predictors_names
        feature_importance = self.__classifiers['xgb'].feature_importances_

        self.feature_importance = {
            Feature_Importance_Fields.PREDICTOR_NAMES: predictor_names,
            Feature_Importance_Fields.FEATURE_IMPORTANCE: feature_importance}
