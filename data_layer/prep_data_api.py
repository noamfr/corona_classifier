import pandas as pd
from get_data_layer.data_fields import Data_Fields


class Prep_Data_Api:
    def __init__(self, patients):
        self.patients = patients

    def prep_data(self):
        self.__one_hot_encoding()

    def __one_hot_encoding(self):
        self.df = pd.get_dummies(data=self.df, columns=Data_Fields.get_binary_vars(), drop_first=True)
