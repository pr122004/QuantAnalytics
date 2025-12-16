import statsmodels.api as sm
import pandas as pd

# Calculate hedge ratio (beta) using OLS regression
def hedge_ratio(y:pd.Series, x: pd.Series) -> float:
    x = sm.add_constant(x)
    model = sm.OLS(y, x, missing="drop").fit()
    return model.params.iloc[1]
