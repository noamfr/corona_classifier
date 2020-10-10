import numpy as np
from typing import List


class Analysis_Vector:
    def __init__(self, field_name: str, vector: np.ndarray, missing_value_idx: List):
        self.field_name = field_name
        self.vector = vector
        self.missing_value_idx = missing_value_idx
