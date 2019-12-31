import numpy as np
from classifier.characteristic import stadistical
from sklearn.externals import joblib

trained_models = {
    "ma": "classifier/model/trained/ma.joblib",
    "he": "classifier/model/trained/he.joblib",
    "hr": "classifier/model/trained/hr.joblib"
}


def classify(green_values_of_lesions, type):
    # Get all the statistical features of each region
    statistical_features_of_lesions = []
    for lesion in green_values_of_lesions:
        statistical_features_of_lesions.append(_get_statistical_features(lesion))

    non_null_data = _clean_data(statistical_features_of_lesions)
    model = _load_trained_model(trained_models[type])
    predicted = model.predict(non_null_data)
    return predicted


def _load_trained_model(model):
    return joblib.load(model)


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
    cleaned_data = []
    for data in data_with_nulls:
        to_append = True
        for val in data:
            if np.isnan(val):
                to_append = False
                break
        if to_append:
            cleaned_data.append(data)
    return np.asarray(cleaned_data)
