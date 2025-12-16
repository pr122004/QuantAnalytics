import pandas as pd

def rolling_correlation(series1: pd.Series, series2: pd.Series, window: int) -> pd.Series:
    return series1.rolling(window).corr(series2)
