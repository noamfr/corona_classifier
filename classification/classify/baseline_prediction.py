import numpy as np

from collections import defaultdict
from typing import Dict, List
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score, GridSearchCV

from classify.classifiers import Classifiers


class Baseline_prediction:
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.__X = X
        self.__y = y
        self.__classifiers = Classifiers().get_classifiers()
        self.__y_preds: Dict = {}

        self.__cross_val_scores: Dict[str, List[float or str]] = {}
        self.__confusion_matrices: Dict[str, np.ndarray] = {}

        self.__calc()

    def __calc(self):
        self.__fit()
        self.__calc_cross_val_scores()
        self.__predict()
        self.__calc_confusion_matrix()

    def __fit(self):
        for name, model in self.__classifiers.items():
            model.fit(self.__X, self.__y)

    def __calc_cross_val_scores(self):
        model_metrics_dict = defaultdict(list)

        for name, model in self.__classifiers.items():
            f1 = cross_val_score(model,         self.__X, self.__y, cv=5, scoring='f1')
            accuracy = cross_val_score(model,   self.__X, self.__y, cv=5, scoring='accuracy')
            recall = cross_val_score(model,     self.__X, self.__y, cv=5, scoring='recall')
            precision = cross_val_score(model,  self.__X, self.__y, cv=5, scoring='precision')

            model_metrics_dict['model_name'].append(name)
            model_metrics_dict['f1'].append(round(f1.mean(), 2))
            model_metrics_dict['accuracy'].append(round(accuracy.mean(), 2))
            model_metrics_dict['recall'].append(round(recall.mean(), 2))
            model_metrics_dict['precision'].append(round(precision.mean(), 2))

        self.__cross_val_scores = dict(model_metrics_dict)

    def __predict(self):
        y_preds = {}

        for name, model in self.__classifiers.items():
            y_preds[name] = model.predict(self.__X)

        self.__y_preds = y_preds

    def __calc_confusion_matrix(self):
        confusion_matrices = {}

        for model_name, y_pred in self.__y_preds.items():
            cm = confusion_matrix(y_true=self.__y,
                                  y_pred=y_pred)

            confusion_matrices[model_name] = cm

        self.__confusion_matrices = dict(confusion_matrices)

    def __accuracy_ratio_metric(self):
        pass

    @property
    def get_cross_val_scores(self):
        return self.__cross_val_scores

    @property
    def get_confusion_matrices(self):
        return self.__confusion_matrices

