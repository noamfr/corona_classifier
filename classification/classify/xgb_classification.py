import numpy as np
from collections import defaultdict
from sklearn.model_selection import GridSearchCV
from typing import Dict, List
import pandas as pd
from xgboost import XGBClassifier

from .model_assesment import Model_Assessment
from .table_fields import Model_Performance_Fields, Feature_Importance_Fields
from configuration.classification_config import Classification_Config as Config
from data.data import Data
from configuration.classification_config import Classification_Config as Config


class Xgb_Classification:
    def __init__(self, data: Data):
        self.__data = data
        self.xgb = XGBClassifier(seed=42)

        self.__X_train: np.ndarray = data.X_train
        self.__y_train: np.ndarray = data.y_train
        self.__X_val: np.ndarray = data.X_val
        self.__y_val: np.ndarray = data.y_val

        self.__y_pred_proba: np.ndarray = np.array([])
        self.model_performance_for_thresholds: Dict[str, List] = {}
        self.feature_importance: Dict[str, List] = {}

        self.__base_model: XGBClassifier = XGBClassifier(seed=143)
        self.base_model_performance: Dict[str, List] = {}

        self.__calc_base_model()
        self.__tune_learning_rate()
        self.__tune_n_estimators()

    def __calc_base_model(self):
        self.__fit_base_model()
        pred_proba = self.__calc_pred_proba(self.__base_model, self.__X_train)
        self.base_model_performance = self.__calc_model_performance(y=self.__y_train, pred_proba=pred_proba)

    def __fit_base_model(self):
        # self.__base_model = XGBClassifier(
        #     learning_rate=Config.XGB_BASE_MODEL_VALUES['learning_rate'],
        #     n_estimators=Config.XGB_BASE_MODEL_VALUES['n_estimators'],
        #     max_depth=Config.XGB_BASE_MODEL_VALUES['max_depth'],
        #     min_child_weight=Config.XGB_BASE_MODEL_VALUES['min_child_weight'],
        #     gamma=Config.XGB_BASE_MODEL_VALUES['gamma'],
        #     colsample_bytree=Config.XGB_BASE_MODEL_VALUES['colsample_bytree'],
        #     scale_pos_weight=Config.XGB_BASE_MODEL_VALUES['scale_pos_weight'],
        #     random_state=Config.XGB_BASE_MODEL_VALUES['random_state']
        # )

        self.__base_model.fit(self.__X_train, self.__y_train)

    @staticmethod
    def __calc_pred_proba(model: XGBClassifier, X: np.ndarray):
        raw_pred_proba = model.predict_proba(X)
        covid_positive_pred_proba = np.array([proba[1] for proba in raw_pred_proba])

        return covid_positive_pred_proba

    def __calc_model_performance(self, y: np.ndarray, pred_proba: np.ndarray):
        y_true = y
        pred_proba = pred_proba
        model_performance = defaultdict(list)

        for threshold in Config.MODEL_THRESHOLDS:
            y_pred = self.__calc_y_pred_with_threshold(pred_proba, threshold)
            model_assessment = Model_Assessment(y_true=y_true, y_pred=y_pred)

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

    def __tune_learning_rate(self):
        # xgb_model = XGBClassifier(random_state=42, n_estimators=300)
        param_grid = {'learning_rate': [0.01, 0.05, 0.1, 0.3, 0.5, 0.8]}
        clf = GridSearchCV(self.__base_model, param_grid, scoring='recall', n_jobs=-1, verbose=1)
        clf.fit(self.__X_train, self.__y_train)

        results = clf.cv_results_
        df = pd.DataFrame(clf.cv_results_)
        df_short = df[['params', 'mean_test_score', 'rank_test_score']]
        df_short.columns

        best_learning_rate_value = list(clf.best_params_.values())[0]
        self.__base_model = XGBClassifier(seed=143, learning_rate=best_learning_rate_value)
        print(clf.best_params_)
        print(clf.best_score_)

    def __tune_n_estimators(self):
        param_grid = {'n_estimators': [10, 100, 500, 750, 1000]}
        clf = GridSearchCV(self.__base_model, param_grid, scoring='recall', n_jobs=-1, verbose=1)
        clf.fit(self.__X_train, self.__y_train)

        results = clf.cv_results_
        df = pd.DataFrame(clf.cv_results_)
        df_short = df[['params', 'mean_test_score', 'rank_test_score']]
        df_short.columns



