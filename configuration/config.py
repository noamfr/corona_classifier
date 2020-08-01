import os


class Config:
    WORK_DIR: str
    RAW_DATA_PATH: str
    PICKLE_PATH: str
    OUTPUT_PATH: str

    WORK_DIR = 'C:/Users/normy/corona_classifier_files'
    RAW_DATA_PATH = 'C:/Users/normy/PycharmProjects/covidclinicaldata/data'
    PICKLE_PATH = os.path.join(WORK_DIR, 'pickle_files')
    OUTPUT_PATH = os.path.join(WORK_DIR, 'outputs')



