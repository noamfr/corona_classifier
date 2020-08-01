from pipeline.pipeline import Pipeline
from configuration.config import Config

if __name__ == '__main__':

    pipeline = Pipeline()

    pipeline.get_data()
    pipeline.prep_data()
    pipeline.basic_analysis()
    pipeline.run_classification()
