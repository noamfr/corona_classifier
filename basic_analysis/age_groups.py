class Age_Groups:
    BABY = 'baby_(0-2)'
    TODDLER = 'toddler_(3-5)'
    CHILD = 'child_(6-12)'
    ADOLESCENT = 'adolescent_(13-17)'
    ADULT = 'adult_(18+)'

    CHILDREN = 'child_(0-17)'

    ADULT_AGE_GROUP_1 = 'age 18-24'
    ADULT_AGE_GROUP_2 = 'age 25-34'
    ADULT_AGE_GROUP_3 = 'age 35-44'
    ADULT_AGE_GROUP_4 = 'age 45-54'
    ADULT_AGE_GROUP_5 = 'age 55-64'
    ADULT_AGE_GROUP_6 = 'age 65+'

    @classmethod
    def get_age_groups_binary(cls):
        return [Age_Groups.CHILDREN, Age_Groups.ADULT]

    @classmethod
    def get_age_groups(cls):
        return [Age_Groups.BABY, Age_Groups.TODDLER, Age_Groups.CHILD, Age_Groups.ADOLESCENT, Age_Groups.ADULT]

    @classmethod
    def get_adult_age_groups(cls):
        return [Age_Groups.ADULT_AGE_GROUP_1, Age_Groups.ADULT_AGE_GROUP_2, Age_Groups.ADULT_AGE_GROUP_3,
                Age_Groups.ADULT_AGE_GROUP_4, Age_Groups.ADULT_AGE_GROUP_5, Age_Groups.ADULT_AGE_GROUP_6]

    @classmethod
    def get_children_age_groups(cls):
        return [Age_Groups.BABY, Age_Groups.TODDLER, Age_Groups.CHILD, Age_Groups.ADOLESCENT]

    @classmethod
    def get_all__age_groups(cls):
        return Age_Groups.get_children_age_groups() + Age_Groups.get_adult_age_groups()
