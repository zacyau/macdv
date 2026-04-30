import pandas as pd
import numpy as np
import pytest

from app.indicators import calculate_macdv, calculate_rsi14, get_latest_indicators


class TestCalculateMacdv:
    def test_insufficient_data(self):
        s = pd.Series([1.0] * 5)
        result = calculate_macdv(s, s, s)
        assert (result == 0.0).all()

    def test_basic_calculation(self):
        close = pd.Series([10.0] * 26)
        high = pd.Series([11.0] * 26)
        low = pd.Series([9.0] * 26)
        result = calculate_macdv(close, high, low)
        assert len(result) == 26
        assert result.iloc[-1] == pytest.approx(0.0, abs=1e-6)

    def test_trending_up(self):
        close = pd.Series([10.0 + i * 0.5 for i in range(26)])
        high = close + 1.0
        low = close - 1.0
        result = calculate_macdv(close, high, low)
        assert result.iloc[-1] > 0

    def test_trending_down(self):
        close = pd.Series([20.0 - i * 0.5 for i in range(26)])
        high = close + 1.0
        low = close - 1.0
        result = calculate_macdv(close, high, low)
        assert result.iloc[-1] < 0


class TestCalculateRsi14:
    def test_insufficient_data(self):
        s = pd.Series([1.0] * 5)
        result = calculate_rsi14(s)
        assert (result == 0.0).all()

    def test_all_up(self):
        close = pd.Series([10.0 + i for i in range(20)])
        result = calculate_rsi14(close)
        assert result.iloc[-1] > 70

    def test_all_down(self):
        close = pd.Series([30.0 - i for i in range(20)])
        result = calculate_rsi14(close)
        assert result.iloc[-1] < 30

    def test_neutral(self):
        close = pd.Series([20.0] * 20)
        result = calculate_rsi14(close)
        assert result.iloc[-1] == pytest.approx(100.0, abs=1e-6)


class TestGetLatestIndicators:
    def test_empty_df(self):
        df = pd.DataFrame()
        result = get_latest_indicators(df)
        assert result["macdv"] == 0.0
        assert result["rsi14"] == 0.0
        assert result["macdv_trend"] == "neutral"
        assert result["rsi14_signal"] == "neutral"

    def test_rsi_overbought(self):
        close = pd.Series([10.0 + i for i in range(30)])
        high = close + 1.0
        low = close - 1.0
        df = pd.DataFrame({"close": close, "high": high, "low": low})
        result = get_latest_indicators(df)
        assert result["rsi14_signal"] == "overbought"

    def test_rsi_oversold(self):
        close = pd.Series([40.0 - i for i in range(30)])
        high = close + 1.0
        low = close - 1.0
        df = pd.DataFrame({"close": close, "high": high, "low": low})
        result = get_latest_indicators(df)
        assert result["rsi14_signal"] == "oversold"

    def test_macdv_trend_up(self):
        close = pd.Series([10.0 + i * 0.2 for i in range(30)])
        high = close + 1.0
        low = close - 1.0
        df = pd.DataFrame({"close": close, "high": high, "low": low})
        result = get_latest_indicators(df)
        assert result["macdv_trend"] == "strong_up"

    def test_macdv_trend_down(self):
        close = pd.Series([20.0 - i * 0.2 for i in range(30)])
        high = close + 1.0
        low = close - 1.0
        df = pd.DataFrame({"close": close, "high": high, "low": low})
        result = get_latest_indicators(df)
        assert result["macdv_trend"] == "strong_down"
