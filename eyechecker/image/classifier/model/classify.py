from sklearn.externals import joblib


def classifyMA(binary_img):
    # Get the values from the green channel
    green_channel_values = map_coordinates_to_values()
    # Get all the stadistical features of each reagion
    lession_stadistical_features = calculate_features(green_channel_values)

    # Use the classifier and classsify
    ma_model = _load_trained_model("./trained/ma.joblib")
    predicted_ma = ma_model.predict(lession_stadistical_features)
    return predicted_ma


def _load_trained_model(model):
    # Put this in a dictionary
    return joblib.load(model)
