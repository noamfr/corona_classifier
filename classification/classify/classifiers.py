from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier


class Classifiers:
    DECISION_TREE: DecisionTreeClassifier
    RANDOM_FOREST: RandomForestClassifier
    LOGISTIC: LogisticRegression
    XGBOOST: XGBClassifier

    def __init__(self):
        self.__class__.DECISION_TREE = DecisionTreeClassifier()
        self.__class__.RANDOM_FOREST = RandomForestClassifier()
        self.__class__.LOGISTIC = LogisticRegression()
        self.__class__.XGBOOST = XGBClassifier()

    @classmethod
    def get_classifiers(cls):
        return {
            'decision_tree': cls.DECISION_TREE,
            'random_forest': cls.RANDOM_FOREST,
            'logistic': cls.LOGISTIC,
            'xgb': cls.XGBOOST
        }

    @classmethod
    def model_names(cls):
        return list(cls.get_classifiers().keys())
