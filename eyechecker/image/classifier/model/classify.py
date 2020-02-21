from os import getcwd, path
from pathlib import Path

import numpy as np
from sklearn.externals import joblib

from eyechecker.image.classifier.characteristic import stadistical

def classify(green_values_of_lesions, type):
    trained_models = {
        "ma": "ma.joblib",
        "he": "he.joblib",
        "hr": "hr.joblib"
    }

    # Get all the statistical features of each region
    statistical_features_of_lesions = []
    for lesion in green_values_of_lesions:
        statistical_features_of_lesions.append(_get_statistical_features(lesion))

    statistical_features_of_lesions =  np.asarray(statistical_features_of_lesions)

    non_null_data = _clean_data(statistical_features_of_lesions)
    if not len(non_null_data):
        return []
    model = _load_trained_model(trained_models[type])
    predicted = model.predict(non_null_data)
    return predicted


def _load_trained_model(model):
    current_path = Path(getcwd())
    model_path = path.join(current_path, 'eyechecker', 'image', 'classifier', 'model', 'trained', model)
    return joblib.load(model_path)


def _get_statistical_features(region):
    mean = stadistical.calMean(region)
    standard = stadistical.calStan(region)
    smooth = stadistical.calSmoot(standard)
    skewness = stadistical.csk(region, mean, standard)
    kurt = stadistical.kurtosis(region, mean, standard)
    return [
        mean,
        standard,
        smooth,
        skewness,
        kurt
    ]

def _clean_data(data_with_nulls):
    return data_with_nulls[~np.isnan(data_with_nulls).any(axis=1)]

_all__ = ["classify"]