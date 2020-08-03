from pipeline.pipeline import Pipeline

SAVE_PROGRESS = True


if __name__ == '__main__':

    pipeline = Pipeline()

    pipeline.get_data()
    pipeline.preliminary_analysis()
    pipeline.prep_data()
    pipeline.basic_analysis()
    pipeline.run_classification()