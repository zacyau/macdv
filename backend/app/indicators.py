import pandas as pd
import numpy as np


def calculate_macdv(close: pd.Series, high: pd.Series, low: pd.Series) -> pd.Series:
    if len(close) < 26:
        return pd.Series([0.0] * len(close), index=close.index)

    prev_close = close.shift(1)
    mytr = np.maximum(
        high - low,
        np.maximum(
            (high - prev_close).abs(),
            (low - prev_close).abs()
        )
    )
    atr26 = mytr.rolling(window=26, min_periods=1).mean()
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    diff = ema12 - ema26
    rawvalue = diff / atr26.replace(0, np.nan)
    macdv = np.where(atr26 > 0, rawvalue * 100, 0.0)
    return pd.Series(macdv, index=close.index)


def calculate_rsi14(close: pd.Series) -> pd.Series:
    if len(close) < 14:
        return pd.Series([0.0] * len(close), index=close.index)

    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=14, min_periods=14).mean().copy()
    avg_loss = loss.rolling(window=14, min_periods=14).mean().copy()

    for i in range(14, len(gain)):
        avg_gain.iloc[i] = (avg_gain.iloc[i-1] * 13 + gain.iloc[i]) / 14
        avg_loss.iloc[i] = (avg_loss.iloc[i-1] * 13 + loss.iloc[i]) / 14

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.fillna(100.0)
    return rsi


def get_latest_indicators(df: pd.DataFrame) -> dict:
    if df.empty or len(df) < 26:
        return {
            "macdv": 0.0,
            "rsi14": 0.0,
            "macdv_trend": "neutral",
            "rsi14_signal": "neutral"
        }

    close = df["close"].astype(float)
    high = df["high"].astype(float)
    low = df["low"].astype(float)

    macdv_series = calculate_macdv(close, high, low)
    rsi_series = calculate_rsi14(close)

    latest_macdv = float(macdv_series.iloc[-1])
    latest_rsi = float(rsi_series.iloc[-1])

    if latest_macdv > 150:
        macdv_trend = "momentum_peak"
    elif latest_macdv > 50:
        macdv_trend = "strong_up"
    elif latest_macdv >= -50:
        macdv_trend = "oscillation"
    elif latest_macdv >= -150:
        macdv_trend = "strong_down"
    else:
        macdv_trend = "momentum_decay"

    if latest_rsi > 70:
        rsi_signal = "overbought"
    elif latest_rsi < 30:
        rsi_signal = "oversold"
    else:
        rsi_signal = "neutral"

    return {
        "macdv": round(latest_macdv, 4),
        "rsi14": round(latest_rsi, 4),
        "macdv_trend": macdv_trend,
        "rsi14_signal": rsi_signal
    }
