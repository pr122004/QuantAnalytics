import pandas as pd

# Z score formula : (X - μ) / σ
def compute_zscore(series: pd.Series, window: int) -> pd.Series:
    
    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std()
    return (series - rolling_mean) / rolling_std
