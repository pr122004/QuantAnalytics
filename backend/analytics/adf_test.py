from statsmodels.tsa.stattools import adfuller
import pandas as pd

def adf_test(series: pd.Series) -> dict:
    result = adfuller(series.dropna())
    return {
        "adf_statistic": result[0],
        "p_value": result[1],
    }
#Perform Augmented Dickey-Fuller test to check for stationarity of a time series