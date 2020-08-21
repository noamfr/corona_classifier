from pipeline.pipeline import Pipeline

SAVE_PROGRESS = True


if __name__ == '__main__':

    pipeline = Pipeline()

    pipeline.get_data()
    pipeline.treat_missing_values()
    pipeline.prep_data_old()
    pipeline.basic_analysis()
    pipeline.run_classification()