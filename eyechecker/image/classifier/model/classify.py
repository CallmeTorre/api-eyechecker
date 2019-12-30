from classifier.characteristic import stadistical
from sklearn.externals import joblib


def classifyMA(green_channel_lessions):
    # Get all the stadistical features of each reagion
    stadistical_lessions = []
    for lession in green_channel_lessions:
        stadistical_lessions.append(_get_stadistical_features(lession))

    # TODO Check how this is going to perfom in the server
    ma_model = _load_trained_model("classifier/model/trained/ma.joblib")
    predicted_ma = ma_model.predict(stadistical_lessions)
    return predicted_ma


def _load_trained_model(model):
    # Put this in a dictionary
    return joblib.load(model)


def _get_stadistical_features(region):
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
