from config.config import Config
from analysis.age_analysis.age_groups import Age_Groups


class Patient:
    __slots__ = ['batch_date', 'test_name', 'swab_type', 'covid19_test_results', 'age',
                 'high_risk_exposure_occupation', 'high_risk_interactions', 'diabetes', 'chd', 'htn', 'cancer',
                 'asthma', 'copd', 'autoimmune_dis', 'smoker', 'temperature', 'pulse', 'sys', 'dia', 'rr', 'sats',
                 'rapid_flu_results', 'rapid_strep_results', 'ctab', 'labored_respiration', 'rhonchi', 'wheezes',
                 'days_since_symptom_onset', 'cough', 'cough_severity', 'fever', 'sob', 'sob_severity', 'diarrhea',
                 'fatigue', 'headache', 'loss_of_smell', 'loss_of_taste', 'runny_nose', 'muscle_sore', 'sore_throat',
                 'cxr_findings', 'cxr_impression', 'cxr_label', 'cxr_link', 'er_referral', 'source_file']

    def __init__(self, source_file):
        self.batch_date = None
        self.test_name = None
        self.swab_type = None
        self.covid19_test_results = None
        self.age = None
        self.high_risk_exposure_occupation = None
        self.high_risk_interactions = None
        self.diabetes = None
        self.chd = None
        self.htn = None
        self.cancer = None
        self.asthma = None
        self.copd = None
        self.autoimmune_dis = None
        self.smoker = None
        self.temperature = None
        self.pulse = None
        self.sys = None
        self.dia = None
        self.rr = None
        self.sats = None
        self.rapid_flu_results = None
        self.rapid_strep_results = None
        self.ctab = None
        self.labored_respiration = None
        self.rhonchi = None
        self.wheezes = None
        self.days_since_symptom_onset = None
        self.cough = None
        self.cough_severity = None
        self.fever = None
        self.sob = None
        self.sob_severity = None
        self.diarrhea = None
        self.fatigue = None
        self.headache = None
        self.loss_of_smell = None
        self.loss_of_taste = None
        self.runny_nose = None
        self.muscle_sore = None
        self.sore_throat = None
        self.cxr_findings = None
        self.cxr_impression = None
        self.cxr_label = None
        self.cxr_link = None
        self.er_referral = None
        self.source_file = source_file

    @property
    def is_adult(self):
        if int(self.age) < Config.ADULT_AGE_THRESHOLD:
            return 0

        else:
            return 1

    @property
    def age_category(self):
        if 0 < self.age <= 2:
            return Age_Groups.BABY

        elif 3 < self.age <= 5:
            return Age_Groups.TODDLER

        elif 6 < self.age <= 12:
            return Age_Groups.CHILD

        elif 13 < self.age <= 17:
            return Age_Groups.ADOLESCENT

        elif 18 < self.age <= 24:
            return Age_Groups.AGE_18_24

        elif 25 < self.age <= 34:
            return Age_Groups.AGE_25_34

        elif 35 < self.age <= 44:
            return Age_Groups.AGE_35_44

        elif 45 < self.age <= 54:
            return Age_Groups.AGE_45_54

        elif 55 < self.age <= 64:
            return Age_Groups.AGE_55_64

        elif 65 < self.age <= 99:
            return Age_Groups.AGE_65_99

        else:
            return Age_Groups.AGE_100_OR_MORE
