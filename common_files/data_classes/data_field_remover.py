from typing import List


class Data_field_remover:

    def __init__(self, data_field_class, fields_to_remove: List):
        self.fields_to_remove = fields_to_remove
        self.data_field_class = data_field_class

        self.__remove_date_fields()

    def __remove_date_fields(self):
        for field in self.fields_to_remove:
            getattr(self.data_field_class, field.upper()).in_analysis = False
