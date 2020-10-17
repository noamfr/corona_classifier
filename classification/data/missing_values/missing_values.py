class Missing_Values:
    def __init__(self):
        pass

    def __get_fields_not_in_analysis(self):
        data_fields_not_in_analysis = []
        for idx in range(len(self.data_field_missing_values['data_field'])):
            if self.data_field_missing_values['null_percent'][idx] >= Static_Configs.MISSING_VALUES_THRESHOLD:
                data_fields_not_in_analysis.append(self.data_field_missing_values['data_field'][idx])

        return data_fields_not_in_analysis

    def __remove_fields(self):
        data_field_remover = Data_field_remover(data_field_class=Data_Fields,
                                                fields_to_remove=self.__get_fields_not_in_analysis())
        data_field_remover.remove_date_fields()