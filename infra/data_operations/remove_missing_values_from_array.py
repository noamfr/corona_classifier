import numpy as np


def remove_missing_values_from_array(array):
    idxs_to_remove = []
    for idx in range(len(array)):
        if array[idx] is None:
            idxs_to_remove.append(idx)

    array = [value for idx, value in enumerate(array) if idx not in idxs_to_remove]
    return array
