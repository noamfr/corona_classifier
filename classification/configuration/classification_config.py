import os


class Classification_Config:
    WORK_DIR: str
    RAW_DATA_PATH: str
    PICKLE_PATH: str

    def __init__(self):
        __class__.WORK_DIR = 'C:/Users/normy/corona_classifier_files/classification'
        __class__.RAW_DATA_PATH = 'C:/Users/normy/PycharmProjects/covidclinicaldata/data'
        __class__.PICKLE_PATH = os.path.join(self.WORK_DIR, 'pickle_files')
