import pandas as pd

def price_stats(df : pd.DataFrame) -> dict:
    return {
        "mean_price]" : df["price"].mean(),
        "std_price" : df["price"].std(),
        "max_price" : df["price"].max(),
        "min_price" : df["price"].min()
    }