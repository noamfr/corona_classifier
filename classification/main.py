from pipeline_operations.pipeline_executor import Pipeline_Executor

from configuration.classification_config import Classification_Config
from classification_pipeline import Classification_Pipeline

SAVE_HISTORY = True
SAVE_STATE = True
JOB_KEY = 'corona_classification'
CONFIG = Classification_Config()

if __name__ == '__main__':

    pipeline = Classification_Pipeline()

    steps = [
        pipeline.fetch_patients,
        pipeline.calc_data,
        pipeline.run_classification,
        pipeline.publish
    ]

    pipeline_executor = Pipeline_Executor(pipeline_class=pipeline,
                                          steps=steps,
                                          save_history=SAVE_HISTORY,
                                          save_state=SAVE_STATE,
                                          pickle_path=Classification_Config.PICKLE_PATH,
                                          job_key=JOB_KEY)
    pipeline_executor.execute()
