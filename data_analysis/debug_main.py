from pipeline import Pipeline
from pipeline_operations.pipeline_executor import Pipeline_Executor
from config.data_analysis_config import Data_Analysis_Config

SAVE_HISTORY = True
SAVE_STATE = True
JOB_KEY = 'corona_data_analysis'
CONFIG = Data_Analysis_Config()

if __name__ == '__main__':

    pipeline = Pipeline()

    steps = [
        pipeline.calc_data,
        pipeline.run_analysis,
        pipeline.save_outputs_to_file
    ]

    pipeline_executor = Pipeline_Executor(pipeline_class=pipeline,
                                          steps=steps,
                                          save_history=SAVE_HISTORY,
                                          save_state=SAVE_STATE,
                                          pickle_path=Data_Analysis_Config.PICKLE_PATH,
                                          job_key=JOB_KEY)
    pipeline_executor.execute()
