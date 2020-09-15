from pipeline.pipeline import Pipeline
from pipeline_operations.pipeline_executor import Pipeline_Executor
from config.config import Config

SAVE_PROGRESS = True
JOB_KEY = 'corona_classifier'
CONFIG = Config()

if __name__ == '__main__':

    pipeline = Pipeline()

    steps = [
        'get_data',
        'treat_missing_values',
        'prep_data',
        'exploratory_analysis',
        'run_classification'
    ]

    pipeline_executor = Pipeline_Executor(pipeline_class=pipeline,
                                          steps=steps,
                                          save_progress=SAVE_PROGRESS,
                                          pickle_path=Config.PICKLE_PATH,
                                          job_key=JOB_KEY
                                          )
    pipeline_executor.execute()
