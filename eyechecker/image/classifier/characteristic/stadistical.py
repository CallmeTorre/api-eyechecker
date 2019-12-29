import numpy as np


# Check this https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skew.html
def csk(data, mean, standard):
    total_sum = 0
    for pixel in data:
        total_sum += (pixel - mean) ** 3
    return total_sum / ((len(data)) * (standard) ** 3)


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kurtosis.html
def kurtosis(data, mean, standard):
    total_sum = 0
    for pixel in data:
        total_sum += (pixel - mean) ** 4
    return total_sum / ((len(data) - 1) * (standard) ** 4)


def calMean(data):
    return np.mean(data)


def calStan(data):
    return np.std(data)


def calSmoot(standard):
    return 1 - (1 / (1 + (standard ** 2)))
