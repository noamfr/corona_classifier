import numpy as np
from typing import Dict


class Model_Assessment:
    def __init__(self, y_true: np.ndarray, y_pred: np.ndarray):
        self.__y_true = y_true
        self.__y_pred = y_pred
        self.confusion_matrix: Dict = {}
        self.model_metrics: Dict = {}

        self.__calc()

    def __calc(self):
        self.__calc_confusion_matrix()
        self.__calc_model_metrics()

    def __calc_confusion_matrix(self):
        true_positive = 0
        false_positive = 0
        true_negative = 0
        false_negative = 0

        for idx in range(len(self.__y_pred)):
            if self.__y_pred[idx] == 1 and self.__y_true[idx] == 1:
                true_positive += 1

            if self.__y_pred[idx] == 1 and self.__y_true[idx] == 0:
                false_positive += 1

            if self.__y_pred[idx] == 0 and self.__y_true[idx] == 0:
                true_negative += 1

            if self.__y_pred[idx] == 0 and self.__y_true[idx] == 1:
                false_negative += 1

        self.confusion_matrix = {
            'true_positive': true_positive,
            'false_positive': false_positive,
            'true_negative': true_negative,
            'false_negative': false_negative
        }

    def __calc_model_metrics(self):
        true_positive, false_positive, true_negative, false_negative = self.confusion_matrix.values()

        if true_positive + false_negative == 0:
            recall = None
        else:
            recall = true_positive / (true_positive + false_negative)

        if true_positive + false_positive == 0:
            precision = None
        else:
            precision = true_positive / (true_positive + false_positive)

        if precision is None or recall is None or precision + recall == 0:
            f1_score = None
        else:
            f1_score = (2 * precision * recall) / (precision + recall)

        accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)

        self.model_metrics = {
            'recall': recall,
            'precision': precision,
            'accuracy': accuracy,
            'f1_score': f1_score
        }

    @property
    def true_positive(self):
        return self.confusion_matrix['true_positive']

    @property
    def false_positive(self):
        return self.confusion_matrix['false_positive']

    @property
    def true_negative(self):
        return self.confusion_matrix['true_negative']

    @property
    def false_negative(self):
        return self.confusion_matrix['false_negative']

    @property
    def recall(self):
        return self.model_metrics['recall']

    @property
    def precision(self):
        return self.model_metrics['precision']

    @property
    def accuracy(self):
        return self.model_metrics['accuracy']

    @property
    def f1_score(self):
        return self.model_metrics['f1_score']
