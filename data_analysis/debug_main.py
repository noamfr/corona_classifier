from pipeline import Pipeline
from pipeline_operations.pipeline_executor import Pipeline_Executor
from config.config import Config

SAVE_HISTORY = True
SAVE_STATE = True
JOB_KEY = 'corona_classifier'
CONFIG = Config()

if __name__ == '__main__':

    pipeline = Pipeline()

    steps = [
        # 'get_data',
        'run_analysis',
        'save_outputs_to_file'
    ]

    pipeline_executor = Pipeline_Executor(pipeline_object=pipeline,
                                          steps=steps,
                                          save_history=SAVE_HISTORY,
                                          save_state=SAVE_STATE,
                                          pickle_path=Config.PICKLE_PATH,
                                          job_key=JOB_KEY)
    pipeline_executor.execute()
