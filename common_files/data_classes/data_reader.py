import csv
from typing import List
from os import listdir, path

from .patient import Patient
from .new_patient import New_Patient
from .data_fields import Data_Fields


class Data_Reader:
    def __init__(self, raw_data_path: str):
        self.patients: List = []
        self.raw_data_path = raw_data_path

        self.__get_patients()

    def __get_patients(self):
        for file_name in listdir(self.raw_data_path):
            reader = csv.DictReader(open(path.join(self.raw_data_path, file_name)))

            for row in reader:
                if 'batch_date' in row.keys():
                    batch_date = 'batch_date'
                else:
                    batch_date = 'ן»¿batch_date'

                self.patients.append(
                    New_Patient(
                        batch_date=str(row[batch_date]),
                        test_name=str(row[Data_Fields.TEST_NAME.field_name]),
                        swab_type=str(row[Data_Fields.SWAB_TYPE.field_name]),
                        covid19_test_results=row[Data_Fields.COVID19_TEST_RESULTS.field_name],
                        age=int(row[Data_Fields.AGE.field_name]),
                        high_risk_exposure_occupation=row[Data_Fields.HIGH_RISK_EXPOSURE_OCCUPATION.field_name],
                        high_risk_interactions=row[Data_Fields.HIGH_RISK_INTERACTIONS.field_name],
                        diabetes=row[Data_Fields.DIABETES.field_name],
                        chd=row[Data_Fields.CHD.field_name],
                        htn=row[Data_Fields.HTN.field_name],
                        cancer=row[Data_Fields.CANCER.field_name],
                        asthma=row[Data_Fields.ASTHMA.field_name],
                        copd=row[Data_Fields.COPD.field_name],
                        autoimmune_dis=row[Data_Fields.AUTOIMMUNE_DIS.field_name],
                        smoker=row[Data_Fields.SMOKER.field_name],
                        temperature=self.__num_string_to_int_or_float(row[Data_Fields.TEMPERATURE.field_name]),
                        pulse=self.__num_string_to_int_or_float(row[Data_Fields.PULSE.field_name]),
                        sys=self.__num_string_to_int_or_float(row[Data_Fields.SYS.field_name]),
                        dia=self.__num_string_to_int_or_float(row[Data_Fields.DIA.field_name]),
                        rr=self.__num_string_to_int_or_float(row[Data_Fields.RR.field_name]),
                        sats=self.__num_string_to_int_or_float(row[Data_Fields.SATS.field_name]),
                        rapid_flu_results=row[Data_Fields.RAPID_FLU_RESULTS.field_name],
                        rapid_strep_results=row[Data_Fields.RAPID_STREP_RESULTS.field_name],
                        ctab=row[Data_Fields.CTAB.field_name],
                        labored_respiration=row[Data_Fields.LABORED_RESPIRATION.field_name],
                        rhonchi=row[Data_Fields.RHONCHI.field_name],
                        wheezes=row[Data_Fields.WHEEZES.field_name],
                        days_since_symptom_onset=self.__num_string_to_int_or_float(
                            row[Data_Fields.DAYS_SINCE_SYMPTOM_ONSET.field_name]),
                        cough=row[Data_Fields.COUGH.field_name],
                        cough_severity=str(row[Data_Fields.COUGH_SEVERITY.field_name]),
                        fever=row[Data_Fields.FEVER.field_name],
                        sob=row[Data_Fields.SOB.field_name],
                        sob_severity=row[Data_Fields.SOB_SEVERITY.field_name],
                        diarrhea=row[Data_Fields.DIARRHEA.field_name],
                        fatigue=row[Data_Fields.FATIGUE.field_name],
                        headache=row[Data_Fields.HEADACHE.field_name],
                        loss_of_smell=row[Data_Fields.LOSS_OF_SMELL.field_name],
                        loss_of_taste=row[Data_Fields.LOSS_OF_TASTE.field_name],
                        runny_nose=row[Data_Fields.RUNNY_NOSE.field_name],
                        muscle_sore=row[Data_Fields.MUSCLE_SORE.field_name],
                        sore_throat=row[Data_Fields.SORE_THROAT.field_name],
                        cxr_findings=row[Data_Fields.CXR_FINDINGS.field_name],
                        cxr_impression=row[Data_Fields.CXR_IMPRESSION.field_name],
                        cxr_label=row[Data_Fields.CXR_LABEL.field_name],
                        cxr_link=row[Data_Fields.CXR_LINK.field_name],
                        er_referral=None,
                        source_file=file_name
                    )
                )

    @staticmethod
    def __num_string_to_int_or_float(num_string: str):
        if num_string.isdigit():
            return int(num_string)

        else:
            try:
                float(num_string)
                return float(num_string)

            except ValueError:
                return num_string
    #
    # def get_patients_old(self):
    #     all_data_fields = Data_Fields.get_all_data_fields()
    #     patients = []
    #
    #     for file_name in listdir(self.raw_data_path):
    #         reader = csv.DictReader(open(path.join(self.raw_data_path, file_name)))
    #
    #         for row in reader:
    #             patient = Patient(source_file=file_name)
    #             key_list = list(row.keys())
    #
    #             for idx in range(len(key_list)):
    #                 if row[key_list[idx]] == '':
    #                     setattr(patient, all_data_fields[idx], None)
    #
    #                 elif key_list[idx] == Data_Fields.AGE.field_name:
    #                     setattr(patient, all_data_fields[idx], int(row[key_list[idx]]))
    #
    #                 elif key_list[idx] in {
    #                     Data_Fields.TEMPERATURE.field_name,
    #                     Data_Fields.PULSE.field_name,
    #                     Data_Fields.SYS.field_name,
    #                     Data_Fields.DIA.field_name,
    #                     Data_Fields.RR.field_name,
    #                     Data_Fields.SATS.field_name,
    #                     Data_Fields.DAYS_SINCE_SYMPTOM_ONSET.field_name
    #                 }:
    #                     setattr(patient, all_data_fields[idx], float(row[key_list[idx]]))
    #
    #                 else:
    #                     setattr(patient, all_data_fields[idx], row[key_list[idx]])
    #
    #             patients.append(patient)
    #
    #     return patients
