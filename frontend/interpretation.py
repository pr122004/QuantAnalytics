import pandas as pd


def interpret_zscore(z, threshold):
    if pd.isna(z):
        return (
            "Insufficient historical data to interpret the spread behaviour."
        )

    if abs(z) < threshold:
        return (
            f"Spread deviation ({z:.2f}) is within the normal range. "
            "No strong mean-reversion signal at this level."
        )

    if z > 0:
        return (
            f"Spread is elevated (z = {z:.2f}). "
            "This may indicate a potential short-spread setup "
            "if the relationship remains stable."
        )

    return (
        f"Spread is compressed (z = {z:.2f}). "
        "This may indicate a potential long-spread setup "
        "if the relationship remains stable."
    )


def interpret_correlation(corr):
    if pd.isna(corr):
        return "Correlation unavailable due to insufficient data."

    if corr >= 0.7:
        return (
            f"Rolling correlation is strong ({corr:.2f}). "
            "The pair relationship appears stable."
        )

    if corr >= 0.4:
        return (
            f"Rolling correlation is moderate ({corr:.2f}). "
            "Signals should be treated cautiously."
        )

    return (
        f"Rolling correlation is weak ({corr:.2f}). "
        "Mean-reversion assumptions may not hold."
    )


def next_steps_guidance(z, corr, threshold):
    steps = []

    if pd.isna(z) or pd.isna(corr):
        return [
            "Wait for additional data before drawing conclusions.",
            "Avoid acting on incomplete signals.",
        ]

    if abs(z) < threshold:
        steps.append(
            "Monitor the spread for larger deviations from the mean."
        )
    else:
        steps.append(
            "Observe whether the spread begins to revert toward its mean."
        )

    if corr < 0.6:
        steps.append(
            "Re-evaluate the pair due to weakening correlation."
        )
    else:
        steps.append(
            "Confirm correlation stability over longer windows."
        )

    steps.append(
        "Validate stationarity before acting on signals."
    )

    return steps
