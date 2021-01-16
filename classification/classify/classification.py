import numpy as np
from collections import defaultdict
from typing import Dict, List
from xgboost import XGBClassifier

from configuration.classification_config import Classification_Config as Config
from data.data import Data
from .classifiers import Classifiers
from .model_assesment import Model_Assessment
from .table_fields import Model_Performance_Fields, Feature_Importance_Fields


class Classification:
    def __init__(self, data: Data):
        self.__data = data
        self.__classifiers: Dict[str, XGBClassifier or object] = {}
        self.__X_train: np.ndarray = data.X_train
        self.__y_train: np.ndarray = data.y_train
        self.__X_val: np.ndarray = data.X_val
        self.__y_val: np.ndarray = data.y_val

        self.__y_pred_probas_train: Dict[str, np.ndarray] = {}
        self.model_performance_for_thresholds_train: Dict[str, List] = {}
        self.feature_importance_train: Dict[str, List] = {}

        self.__y_pred_probas_val: Dict[str, np.ndarray] = {}
        self.model_performance_for_thresholds_val: Dict[str, List] = {}

        self.__calc()

    def __calc(self):
        self.__get_classifiers()
        self.__fit_training_set()
        self.__predict_proba_training_set()
        self.__calc_model_performance_for_thresholds_training_set()
        self.__calc_feature_importance()
        self.__predict_proba_val_set()
        self.__calc_model_performance_for_thresholds_val()

    def __get_classifiers(self):
        self.__classifiers = Classifiers().get_classifiers()

    def __fit_training_set(self):
        for name, model in self.__classifiers.items():
            model.fit(self.__X_train, self.__y_train)

    def __predict_proba_training_set(self):
        self.__y_pred_probas_train = self.__predict_proba(classifiers=self.__classifiers,
                                                          X_set=self.__X_train)

    @staticmethod
    def __predict_proba(classifiers: Dict[str, XGBClassifier or object], X_set: np.ndarray):
        y_preds = {}

        for name, model in classifiers.items():
            preds = model.predict_proba(X_set)
            preds_covid_positive = np.array([pred[1] for pred in preds])
            y_preds[name] = preds_covid_positive

        return y_preds

    def __calc_model_performance_for_thresholds_training_set(self):
        model_performance = defaultdict(list)
        y_true = self.__y_train

        for model_name, y_pred_proba in self.__y_pred_probas_train.items():
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

        self.model_performance_for_thresholds_train = dict(model_performance)

    def __calc_feature_importance(self):
        predictor_names = self.__data.predictors_names
        metrics = {
            'gain': self.__classifiers['xgb'].get_booster().get_score(importance_type="gain"),
            'weight': self.__classifiers['xgb'].get_booster().get_score(importance_type="weight"),
            'cover': self.__classifiers['xgb'].get_booster().get_score(importance_type="cover"),
            'total_gain': self.__classifiers['xgb'].get_booster().get_score(importance_type="total_gain"),
            'total_cover': self.__classifiers['xgb'].get_booster().get_score(importance_type="total_cover")
        }
        feature_importance_dict = defaultdict(list)

        for feature_number in metrics['gain'].keys():
            predictor_name = predictor_names[int(feature_number.split('f')[1])]
            feature_importance_dict['predictor name'].append(predictor_name)

            for metric in metrics:
                feature_importance = metrics[metric][feature_number]
                feature_importance_dict[metric].append(feature_importance)

        self.feature_importance_train = dict(feature_importance_dict)

    def __predict_proba_val_set(self):
        self.__y_pred_probas_val = self.__predict_proba(classifiers=self.__classifiers,
                                                        X_set=self.__X_val)

    def __calc_model_performance_for_thresholds_val(self):
        self.model_performance_for_thresholds_val = self.__calc_model_performance_for_thresholds(
            y_true=self.__y_val,
            y_pred_probas=self.__y_pred_probas_val
        )

    def __calc_model_performance_for_thresholds(self, y_true: np.ndarray, y_pred_probas: Dict[str, np.ndarray]):
        model_performance = defaultdict(list)

        for model_name, y_pred_proba in y_pred_probas.items():
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

        return dict(model_performance)

    @staticmethod
    def __calc_y_pred_with_threshold(y_pred_proba: np.ndarray, threshold: float):
        y_preds = []

        for idx in range(len(y_pred_proba)):
            covid_positive_probability = y_pred_proba[idx]
            if covid_positive_probability > threshold:
                y_pred = 1

            else:
                y_pred = 0

            y_preds.append(y_pred)

        return np.array(y_preds)

    def __tune_XGB_hyper_parameters(self):
        xgb = self.__classifiers['xgb']
