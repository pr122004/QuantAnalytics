import pandas as pd

#spresad = Y - beta * X
def compute_spread(price_y: pd.Series, price_x: pd.Series, beta: float) -> pd.Series:
    return price_y - beta * price_x