import csv
from os import listdir, path
from config.config import Config
from .patient import Patient
from .data_fields import Data_Fields


class Data_Reader:
    def __init__(self):
        self.patients = []

    @staticmethod
    def get_patients():
        all_data_fields = Data_Fields.get_all_data_fields()
        patients = []

        for file_name in listdir(Config.RAW_DATA_PATH):
            reader = csv.DictReader(open(path.join(Config.RAW_DATA_PATH, file_name)))

            for row in reader:
                patient = Patient(source_file=file_name)
                key_list = list(row.keys())

                for idx in range(len(key_list)):
                    if row[key_list[idx]] == '':
                        setattr(patient, all_data_fields[idx], None)

                    elif key_list[idx] == 'age':
                        setattr(patient, all_data_fields[idx], int(row[key_list[idx]]))

                    else:
                        setattr(patient, all_data_fields[idx], row[key_list[idx]])

                patients.append(patient)

        return patients
