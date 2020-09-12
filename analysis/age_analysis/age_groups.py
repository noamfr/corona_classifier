class Age_Groups:
    BABY = 'baby_(0-2)'
    TODDLER = 'toddler_(3-5)'
    CHILD = 'child_(6-12)'
    ADOLESCENT = 'adolescent_(13-17)'

    CHILDREN = 'child_(0-17)'
    ADULT = 'adult_(18+)'

    AGE_18_24 = 'age 18-24'
    AGE_25_34 = 'age 25-34'
    AGE_35_44 = 'age 35-44'
    AGE_45_54 = 'age 45-54'
    AGE_55_64 = 'age 55-64'
    AGE_65_99 = 'age 65-99'
    AGE_100_OR_MORE = 'age_100_or_more'

    @classmethod
    def age_groups_binary(cls):
        return [Age_Groups.CHILDREN, Age_Groups.ADULT]

    @classmethod
    def get_age_groups(cls):
        return [Age_Groups.BABY, Age_Groups.TODDLER, Age_Groups.CHILD, Age_Groups.ADOLESCENT, Age_Groups.ADULT]

    @classmethod
    def get_adult_age_groups(cls):
        return [Age_Groups.AGE_18_24, Age_Groups.AGE_25_34, Age_Groups.AGE_35_44,
                Age_Groups.AGE_45_54, Age_Groups.AGE_55_64, Age_Groups.AGE_65_99]

    @classmethod
    def get_children_age_groups(cls):
        return [Age_Groups.BABY, Age_Groups.TODDLER, Age_Groups.CHILD, Age_Groups.ADOLESCENT]

    @classmethod
    def get_all__age_groups(cls):
        return Age_Groups.get_children_age_groups() + Age_Groups.get_adult_age_groups()

    @classmethod
    def children_and_adult_age_groups(cls):
        return [Age_Groups.CHILDREN] + Age_Groups.get_adult_age_groups()
