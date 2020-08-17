from enum import Enum


class Data_Classes:
    BINARY = 'binary'
    CATEGORICAL = 'categorical'
    CONTINUOUS = 'continuous'
    TEXT = 'text'
    NOT_IN_USE = 'not_in_use'

    class Data_Classes_a:
        BINARY: str
        CATEGORICAL: str
        CONTINUOUS: str
        TEXT: str
        NOT_IN_USE: str

        def __init__(self):
            __class__BINARY = 'binary'
            __class__CATEGORICAL = 'categorical'
            __class__CONTINUOUS = 'continuous'
            __class__TEXT = 'text'
            __class__NOT_IN_USE = 'not_in_use'


class Data_Fields(Enum):
    BATCH_DATE = ('batch_date', Data_Classes.CATEGORICAL)
    TEST_NAME = ('test_name', Data_Classes.CATEGORICAL)
    SWAB_TYPE = ('swab_type', Data_Classes.CATEGORICAL)
    COVID19_TEST_RESULTS = ('covid19_test_results', Data_Classes.BINARY)
    AGE = ('age', Data_Classes.CONTINUOUS)
    HIGH_RISK_EXPOSURE_OCCUPATION = ('high_risk_exposure_occupation', Data_Classes.BINARY)
    HIGH_RISK_INTERACTIONS = ('high_risk_interactions', Data_Classes.BINARY)
    DIABETES = ('diabetes', Data_Classes.BINARY)
    CHD = ('chd', Data_Classes.BINARY)
    HTN = ('htn', Data_Classes.BINARY)
    CANCER = ('cancer', Data_Classes.BINARY)
    ASTHMA = ('asthma', Data_Classes.BINARY)
    COPD = ('copd', Data_Classes.BINARY)
    AUTOIMMUNE_DIS = ('autoimmune_dis', Data_Classes.BINARY)
    SMOKER = ('smoker', Data_Classes.BINARY)
    TEMPERATURE = ('temperature', Data_Classes.CONTINUOUS)
    PULSE = ('pulse', Data_Classes.CONTINUOUS)
    SYS = ('sys', Data_Classes.CONTINUOUS)
    DIA = ('dia', Data_Classes.CONTINUOUS)
    RR = ('rr', Data_Classes.CONTINUOUS)
    SATS = ('sats', Data_Classes.CONTINUOUS)
    RAPID_FLU_RESULTS = ('rapid_flu_results', Data_Classes.BINARY)
    RAPID_STREP_RESULTS = ('rapid_strep_results', Data_Classes.BINARY)
    CTAB = ('ctab', Data_Classes.BINARY)
    LABORED_RESPIRATION = ('labored_respiration', Data_Classes.BINARY)
    RHONCHI = ('rhonchi', Data_Classes.BINARY)
    WHEEZES = ('wheezes', Data_Classes.BINARY)
    DAYS_SINCE_SYMPTOM_ONSET = ('days_since_symptom_onset', Data_Classes.CONTINUOUS)
    COUGH = ('cough', Data_Classes.BINARY)
    COUGH_SEVERITY = ('cough_severity', Data_Classes.CATEGORICAL)
    FEVER = ('fever', Data_Classes.BINARY)
    SOB = ('sob', Data_Classes.BINARY)
    SOB_SEVERITY = ('sob_severity', Data_Classes.CATEGORICAL)
    DIARRHEA = ('diarrhea', Data_Classes.BINARY)
    FATIGUE = ('fatigue', Data_Classes.BINARY)
    HEADACHE = ('headache', Data_Classes.BINARY)
    LOSS_OF_SMELL = ('loss_of_smell', Data_Classes.BINARY)
    LOSS_OF_TASTE = ('loss_of_taste', Data_Classes.BINARY)
    RUNNY_NOSE = ('runny_nose', Data_Classes.BINARY)
    MUSCLE_SORE = ('muscle_sore', Data_Classes.BINARY)
    SORE_THROAT = ('sore_throat', Data_Classes.BINARY)
    CXR_FINDINGS = ('cxr_findings', Data_Classes.TEXT)
    CXR_IMPRESSION = ('cxr_impression', Data_Classes.CATEGORICAL)
    CXR_LABEL = ('cxr_label', Data_Classes.BINARY)
    CXR_LINK = ('cxr_link', Data_Classes.TEXT)
    ER_REFERRAL = ('er_referral', Data_Classes.NOT_IN_USE)
    SOURCE_FILE = ('source_file', Data_Classes.CATEGORICAL)

    def __init__(self, field_name, data_class):
        self.field_name = field_name
        self.data_class = data_class

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
            if getattr(Data_Fields, var_name.upper()).data_class == Data_Classes.BINARY:
                binary_vars.append(var_name)
        return binary_vars

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
