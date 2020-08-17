from pipeline.pipeline import Pipeline
from infra.pipeline_executor import Pipeline_Executor
from configuration.config import Config

SAVE_PROGRESS = True
JOB_KEY = 'corona_classifier'

if __name__ == '__main__':

    pipeline = Pipeline()

    steps = [
        'get_data',
        'prep_data',
        'basic_analysis',
        'run_classification'
    ]

    pipeline_executor = Pipeline_Executor(pipeline_class=pipeline,
                                          steps=steps,
                                          save_progress=SAVE_PROGRESS,
                                          pickle_path=Config.PICKLE_PATH,
                                          job_key=JOB_KEY
                                          )
    pipeline_executor.execute()
