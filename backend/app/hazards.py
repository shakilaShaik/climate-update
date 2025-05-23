import pandas as pd

def detect_heatwaves(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify heatwave events: 3+ consecutive days with max temp > 95th percentile.
    Returns a DataFrame of heatwave events with start/end/duration.
    """
    if df.empty:
        return pd.DataFrame()

    threshold = df["temp_max"].quantile(0.95)
    df["is_hot"] = df["temp_max"] > threshold

    heatwave_events = []
    start = None
    streak = 0

    for i in range(len(df)):
        if df.iloc[i]["is_hot"]:
            if start is None:
                start = df.iloc[i]["date"]
            streak += 1
        else:
            if streak >= 3:
                end = df.iloc[i - 1]["date"]
                heatwave_events.append({
                    "start": start,
                    "end": end,
                    "duration_days": (end - start).days + 1
                })
            start = None
            streak = 0

    # Final check if heatwave ends at the last row
    if streak >= 3:
        end = df.iloc[-1]["date"]
        heatwave_events.append({
            "start": start,
            "end": end,
            "duration_days": (end - start).days + 1
        })

    return pd.DataFrame(heatwave_events)
