from typing import Dict
from collections import defaultdict
import numpy as np
import pandas as pd


class Descriptive_Table:
    def __init__(self, vector_dict: Dict[str, np.array]):
        self.__vector_dict = vector_dict

    def get_descriptive_table(self):
        data_dict = defaultdict(list)

        for field in self.__vector_dict:
            vector = self.__vector_dict[field]

            count = len(vector)
            avg = vector.mean()
            std = vector.std()
            minimum = vector.min()
            q1 = np.quantile(vector, 0.25)
            median = np.quantile(vector, 0.50)
            q3 = np.quantile(vector, 0.75)
            maximum = vector.max()

            data_dict['field'].append(field)
            data_dict['count'].append(count)
            data_dict['mean'].append(avg)
            data_dict['std'].append(std)
            data_dict['min'].append(minimum)
            data_dict['q1'].append(q1)
            data_dict['median'].append(median)
            data_dict['q3'].append(q3)
            data_dict['max'].append(maximum)

        df = pd.DataFrame(data_dict)
        return df
