

class Vitals_Names:
    TEMPERATURE = 'temperature'
    PULSE = 'pulse'
    SYS = 'sys'
    DIA = 'dia'
    RR = 'rr'
    SATS = 'sats'


class Threshold_Type:
    LOWER = 'lower'
    UPPER = 'upper'


class Threshold_Category:
    ACCEPTED = 'accepted_values'
    HEALTHY = 'healthy_values'


class Population:
    CHILDREN = 'children'
    ADULTS = 'adults'


class Vital_Values:
    def __init__(self, population, threshold_category, threshold_type, temperature, pulse, sys, dia, rr, sats):
        self.population = population
        self.threshold_category = threshold_category
        self.threshold_type = threshold_type
        self.temperature = temperature
        self.pulse = pulse
        self.sys = sys
        self.dia = dia
        self.rr = rr
        self.sats = sats


class Vitals_Container:
    def __init__(self):
        self.children_healthy_lower = Vital_Values
        self.children_healthy_upper = Vital_Values
        self.adults_healthy_lower = Vital_Values
        self.adults_healthy_upper = Vital_Values
        self.vitals_list = []

    def get_vital(self, population, threshold_category, threshold_type, vital_name):
        for vital in self.vitals_list:
            if vital.population == population:
                if vital.threshold_category == threshold_category:
                    if vital.threshold_type == threshold_type:
                        vital_value = getattr(vital, vital_name)

                        return vital_value
