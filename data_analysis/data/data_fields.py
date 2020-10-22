from enum import Enum


class Data_Classes:
    TARGET = 'target'
    BINARY = 'binary'
    CATEGORICAL = 'categorical'
    CONTINUOUS = 'continuous'
    TEXT = 'text'
    NOT_IN_USE = 'not_in_use'


class Data_Fields(Enum):
    BATCH_DATE = ('batch_date', Data_Classes.CATEGORICAL, True)
    TEST_NAME = ('test_name', Data_Classes.CATEGORICAL, True)
    SWAB_TYPE = ('swab_type', Data_Classes.CATEGORICAL, True)
    COVID19_TEST_RESULTS = ('covid19_test_results', Data_Classes.TARGET, True)
    AGE = ('age', Data_Classes.CONTINUOUS, True)
    HIGH_RISK_EXPOSURE_OCCUPATION = ('high_risk_exposure_occupation', Data_Classes.BINARY, True)
    HIGH_RISK_INTERACTIONS = ('high_risk_interactions', Data_Classes.BINARY, True)
    DIABETES = ('diabetes', Data_Classes.BINARY, True)
    CHD = ('chd', Data_Classes.BINARY, True)
    HTN = ('htn', Data_Classes.BINARY, True)
    CANCER = ('cancer', Data_Classes.BINARY, True)
    ASTHMA = ('asthma', Data_Classes.BINARY, True)
    COPD = ('copd', Data_Classes.BINARY, True)
    AUTOIMMUNE_DIS = ('autoimmune_dis', Data_Classes.BINARY, True)
    SMOKER = ('smoker', Data_Classes.BINARY, True)
    TEMPERATURE = ('temperature', Data_Classes.CONTINUOUS, True)
    PULSE = ('pulse', Data_Classes.CONTINUOUS, True)
    SYS = ('sys', Data_Classes.CONTINUOUS, True)
    DIA = ('dia', Data_Classes.CONTINUOUS, True)
    RR = ('rr', Data_Classes.CONTINUOUS, True)
    SATS = ('sats', Data_Classes.CONTINUOUS, True)
    RAPID_FLU_RESULTS = ('rapid_flu_results', Data_Classes.BINARY, True)
    RAPID_STREP_RESULTS = ('rapid_strep_results', Data_Classes.BINARY, True)
    CTAB = ('ctab', Data_Classes.BINARY, True)
    LABORED_RESPIRATION = ('labored_respiration', Data_Classes.BINARY, True)
    RHONCHI = ('rhonchi', Data_Classes.BINARY, True)
    WHEEZES = ('wheezes', Data_Classes.BINARY, True)
    DAYS_SINCE_SYMPTOM_ONSET = ('days_since_symptom_onset', Data_Classes.CONTINUOUS, True)
    COUGH = ('cough', Data_Classes.BINARY, True)
    COUGH_SEVERITY = ('cough_severity', Data_Classes.CATEGORICAL, True)
    FEVER = ('fever', Data_Classes.BINARY, True)
    SOB = ('sob', Data_Classes.BINARY, True)
    SOB_SEVERITY = ('sob_severity', Data_Classes.CATEGORICAL, True)
    DIARRHEA = ('diarrhea', Data_Classes.BINARY, True)
    FATIGUE = ('fatigue', Data_Classes.BINARY, True)
    HEADACHE = ('headache', Data_Classes.BINARY, True)
    LOSS_OF_SMELL = ('loss_of_smell', Data_Classes.BINARY, True)
    LOSS_OF_TASTE = ('loss_of_taste', Data_Classes.BINARY, True)
    RUNNY_NOSE = ('runny_nose', Data_Classes.BINARY, True)
    MUSCLE_SORE = ('muscle_sore', Data_Classes.BINARY, True)
    SORE_THROAT = ('sore_throat', Data_Classes.BINARY, True)
    CXR_FINDINGS = ('cxr_findings', Data_Classes.TEXT, True)
    CXR_IMPRESSION = ('cxr_impression', Data_Classes.CATEGORICAL, True)
    CXR_LABEL = ('cxr_label', Data_Classes.BINARY, True)
    CXR_LINK = ('cxr_link', Data_Classes.TEXT, True)
    ER_REFERRAL = ('er_referral', Data_Classes.NOT_IN_USE, True)
    SOURCE_FILE = ('source_file', Data_Classes.CATEGORICAL, True)

    def __init__(self, field_name, data_class, in_analysis):
        self.field_name = field_name
        self.data_class = data_class
        self.in_analysis = in_analysis

    @classmethod
    def get_target(cls):
        return Data_Fields.COVID19_TEST_RESULTS.field_name

    @classmethod
    def get_features(cls):
        return [Data_Fields.AGE.field_name,
                Data_Fields.PULSE.field_name]

    @classmethod
    def get_binary_vars(cls):
        binary_vars = []
        for var_name in Data_Fields.get_all_data_fields():
            if getattr(Data_Fields, var_name.upper()).data_class == Data_Classes.BINARY and \
                    getattr(Data_Fields, var_name.upper()).in_analysis:
                binary_vars.append(var_name)
        return binary_vars

    @classmethod
    def get_continuous_vars(cls):
        continuous_vars = []
        for var_name in Data_Fields.get_all_data_fields():
            if getattr(Data_Fields, var_name.upper()).data_class == Data_Classes.CONTINUOUS and \
                    getattr(Data_Fields, var_name.upper()).in_analysis:
                continuous_vars.append(var_name)
        return continuous_vars

    @classmethod
    def get_all_data_fields(cls):
        return [
            Data_Fields.BATCH_DATE.field_name,
            Data_Fields.TEST_NAME.field_name,
            Data_Fields.SWAB_TYPE.field_name,
            Data_Fields.COVID19_TEST_RESULTS.field_name,
            Data_Fields.AGE.field_name,
            Data_Fields.HIGH_RISK_EXPOSURE_OCCUPATION.field_name,
            Data_Fields.HIGH_RISK_INTERACTIONS.field_name,
            Data_Fields.DIABETES.field_name,
            Data_Fields.CHD.field_name,
            Data_Fields.HTN.field_name,
            Data_Fields.CANCER.field_name,
            Data_Fields.ASTHMA.field_name,
            Data_Fields.COPD.field_name,
            Data_Fields.AUTOIMMUNE_DIS.field_name,
            Data_Fields.SMOKER.field_name,
            Data_Fields.TEMPERATURE.field_name,
            Data_Fields.PULSE.field_name,
            Data_Fields.SYS.field_name,
            Data_Fields.DIA.field_name,
            Data_Fields.RR.field_name,
            Data_Fields.SATS.field_name,
            Data_Fields.RAPID_FLU_RESULTS.field_name,
            Data_Fields.RAPID_STREP_RESULTS.field_name,
            Data_Fields.CTAB.field_name,
            Data_Fields.LABORED_RESPIRATION.field_name,
            Data_Fields.RHONCHI.field_name,
            Data_Fields.WHEEZES.field_name,
            Data_Fields.DAYS_SINCE_SYMPTOM_ONSET.field_name,
            Data_Fields.COUGH.field_name,
            Data_Fields.COUGH_SEVERITY.field_name,
            Data_Fields.FEVER.field_name,
            Data_Fields.SOB.field_name,
            Data_Fields.SOB_SEVERITY.field_name,
            Data_Fields.DIARRHEA.field_name,
            Data_Fields.FATIGUE.field_name,
            Data_Fields.HEADACHE.field_name,
            Data_Fields.LOSS_OF_SMELL.field_name,
            Data_Fields.LOSS_OF_TASTE.field_name,
            Data_Fields.RUNNY_NOSE.field_name,
            Data_Fields.MUSCLE_SORE.field_name,
            Data_Fields.SORE_THROAT.field_name,
            Data_Fields.CXR_FINDINGS.field_name,
            Data_Fields.CXR_IMPRESSION.field_name,
            Data_Fields.CXR_LABEL.field_name,
            Data_Fields.CXR_LINK.field_name,
            Data_Fields.ER_REFERRAL.field_name,
            Data_Fields.SOURCE_FILE.field_name
        ]
