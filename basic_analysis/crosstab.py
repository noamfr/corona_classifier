

class Cross_Tab_Binary:
    def __init__(self, vector_1, vector_2):
        self.v1 = vector_1
        self.v2 = vector_2

    @property
    def vector_1_count(self):
        return len(self.v1)

    @property
    def vector_2_count(self):
        return len(self.v2)

    @property
    def vector_1_positive_count(self):
        positive_values = [value for value in self.v1 if value == 1]
        return len(positive_values)

    @property
    def vector_2_positive_count(self):
        positive_values = [value for value in self.v2 if value == 1]
        return len(positive_values)

    @property
    def v1_missing_count(self):
        missing_values = [value for value in self.v1 if value is None]
        return len(missing_values)

    @property
    def v2_missing_count(self):
        missing_values = [value for value in self.v2 if value is None]
        return len(missing_values)

    def get_cross_tab_count(self, v1_binary_value: [0, 1], v2_binary_value: [0, 1]):
        counter = 0
        for idx in range(self.vector_1_count):
            if self.v1[idx] is None or self.v2[idx] is None:
                continue

            if self.v1[idx] == v1_binary_value and self.v2[idx] == v2_binary_value:
                counter += 1

        return counter

    def get_cross_tab_percent(self, v1_binary_value: [0, 1], v2_binary_value: [0, 1]):
        cross_tab_count = self.get_cross_tab_count(v1_binary_value, v2_binary_value)
        return cross_tab_count / (self.vector_2_count - self.v2_missing_count)

    def get_perc_v1_positive_from_all_v2_positives(self):
        v1_positive_v2_positive = self.get_cross_tab_count(v1_binary_value=1, v2_binary_value=1)
        v1_negative_v2_positive = self.get_cross_tab_count(v1_binary_value=0, v2_binary_value=1)

        return v1_positive_v2_positive / (v1_positive_v2_positive + v1_negative_v2_positive)

    def get_perc_v1_positive_from_all_v2_negatives(self):
        v1_positive_v2_negative = self.get_cross_tab_count(v1_binary_value=1, v2_binary_value=0)
        v1_negative_v2_negative = self.get_cross_tab_count(v1_binary_value=0, v2_binary_value=0)

        return v1_positive_v2_negative / (v1_positive_v2_negative + v1_negative_v2_negative)
