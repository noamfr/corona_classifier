import uuid
from .age_groups import Age_Groups


class New_Patient:
    __slots__ = ['id', 'batch_date', 'test_name', 'swab_type', 'covid19_test_results', 'age',
                 'high_risk_exposure_occupation', 'high_risk_interactions', 'diabetes', 'chd', 'htn', 'cancer',
                 'asthma', 'copd', 'autoimmune_dis', 'smoker', 'temperature', 'pulse', 'sys', 'dia', 'rr', 'sats',
                 'rapid_flu_results', 'rapid_strep_results', 'ctab', 'labored_respiration', 'rhonchi', 'wheezes',
                 'days_since_symptom_onset', 'cough', 'cough_severity', 'fever', 'sob', 'sob_severity', 'diarrhea',
                 'fatigue', 'headache', 'loss_of_smell', 'loss_of_taste', 'runny_nose', 'muscle_sore', 'sore_throat',
                 'cxr_findings', 'cxr_impression', 'cxr_label', 'cxr_link', 'er_referral', 'source_file']

    def __init__(self, batch_date, test_name, swab_type, covid19_test_results, age, high_risk_exposure_occupation,
                 high_risk_interactions, diabetes, chd, htn, cancer, asthma, copd, autoimmune_dis, smoker, temperature,
                 pulse, sys, dia, rr, sats, rapid_flu_results, rapid_strep_results, ctab, labored_respiration, rhonchi,
                 wheezes, days_since_symptom_onset, cough, cough_severity, fever, sob, sob_severity, diarrhea, fatigue,
                 headache, loss_of_smell, loss_of_taste, runny_nose, muscle_sore, sore_throat, cxr_findings,
                 cxr_impression, cxr_label, cxr_link, er_referral, source_file):

        self.id: str = str(uuid.uuid4())
        self.batch_date: str = batch_date
        self.test_name: str = test_name
        self.swab_type: str = swab_type
        self.covid19_test_results = covid19_test_results
        self.age: int = age
        self.high_risk_exposure_occupation = high_risk_exposure_occupation
        self.high_risk_interactions = high_risk_interactions
        self.diabetes = diabetes
        self.chd = chd
        self.htn = htn
        self.cancer = cancer
        self.asthma = asthma
        self.copd = copd
        self.autoimmune_dis = autoimmune_dis
        self.smoker = smoker
        self.temperature: float = temperature
        self.pulse: float = pulse
        self.sys: float = sys
        self.dia: float = dia
        self.rr: float = rr
        self.sats: float = sats
        self.rapid_flu_results = rapid_flu_results
        self.rapid_strep_results = rapid_strep_results
        self.ctab = ctab
        self.labored_respiration = labored_respiration
        self.rhonchi = rhonchi
        self.wheezes = wheezes
        self.days_since_symptom_onset: int = days_since_symptom_onset
        self.cough = cough
        self.cough_severity: str = cough_severity
        self.fever = fever
        self.sob = sob
        self.sob_severity = sob_severity
        self.diarrhea = diarrhea
        self.fatigue = fatigue
        self.headache = headache
        self.loss_of_smell = loss_of_smell
        self.loss_of_taste = loss_of_taste
        self.runny_nose = runny_nose
        self.muscle_sore = muscle_sore
        self.sore_throat = sore_throat
        self.cxr_findings = cxr_findings
        self.cxr_impression = cxr_impression
        self.cxr_label = cxr_label
        self.cxr_link = cxr_link
        self.er_referral = er_referral
        self.source_file: str = source_file

    @property
    def is_adult(self):
        if int(self.age) < 18:
            return 0

        else:
            return 1

    @property
    def age_group(self):
        if self.age < 18:
            return 'child'
        else:
            return 'adult'

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
