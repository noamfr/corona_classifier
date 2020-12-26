class Model_Performance_Fields:
    MODEL_NAME = 'model name'
    THRESHOLD = 'threshold'

    TRUE_POSITIVE = 'true positive'
    FALSE_POSITIVE = 'false positive'
    TRUE_NEGATIVE = 'true negative'
    FALSE_NEGATIVE = 'false negative'

    RECALL = 'recall'
    PRECISION = 'precision'
    ACCURACY = 'accuracy'
    F1_SCORE = 'f1_score'

    FIELD_ORDER = [
        MODEL_NAME,
        THRESHOLD,

        RECALL,
        PRECISION,
        F1_SCORE,
        ACCURACY,

        TRUE_POSITIVE,
        FALSE_POSITIVE,
        TRUE_NEGATIVE,
        FALSE_NEGATIVE]


class Feature_Importance_Fields:
    PREDICTOR_NAMES = 'predictor names'
    FEATURE_IMPORTANCE = 'feature importance'

    FIELD_ORDER = [PREDICTOR_NAMES, FEATURE_IMPORTANCE]