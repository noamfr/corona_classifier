import pickle
import logging
from os import path
from infra.timer import Timer


class Pipeline_Executor:
    def __init__(self, pipeline_class, steps, save_progress, pickle_path, job_key):
        self.pipeline = pipeline_class
        self.steps = steps
        self.save_progress = save_progress
        self.pickle_path = pickle_path
        self.job_key = job_key

    def execute(self):
        if self.save_progress:
            self.__run_steps()

        else:
            self.__load_pickle()
            self.__run_steps()

    def __run_steps(self):
        for step in self.steps:
            timer = Timer()
            logging.info("================ Executing: " + step + " ================")
            print("================ Executing: " + step + " ================")
            getattr(self.pipeline, step)()

            logging.info("================ Finished running: " + step + " ================")
            timer.stop_timer()
            print("================ Finished running: " + step + " ================")
            timer.print_elapsed_time()

            if self.save_progress:
                self.__save_pipeline_to_pickle(step)

    def __save_pipeline_to_pickle(self, step):
        logging.info("================ Saving: " + step + " to pickle ================")
        print("================ Saving: " + step + " to pickle ================")
        with open(path.join(self.pickle_path, self.job_key+'.pickle'), 'wb') as handle:
            pickle.dump(obj=self.pipeline, file=handle)

    def __load_pickle(self):
        logging.info("================ Loading pickle file ===========")
        print("================ Loading pickle file ===========")
        file = open(path.join(self.pickle_path, self.job_key+'.pickle'), 'rb')
        self.pipeline = pickle.load(file)
