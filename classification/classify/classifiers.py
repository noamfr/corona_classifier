from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


class Classifiers:
    DECISION_TREE: DecisionTreeClassifier
    RANDOM_FOREST: RandomForestClassifier()
    LOGISTIC: LogisticRegression()

    def __init__(self):
        self.__class__.DECISION_TREE = DecisionTreeClassifier()
        self.__class__.RANDOM_FOREST = RandomForestClassifier()
        self.__class__.LOGISTIC = LogisticRegression()

    @classmethod
    def get_classifiers(cls):
        return {
            'decision_tree': cls.DECISION_TREE,
            'random_forest': cls.RANDOM_FOREST,
            'logistic': cls.LOGISTIC
        }

    @classmethod
    def model_names(cls):
        return list(cls.get_classifiers().keys())
