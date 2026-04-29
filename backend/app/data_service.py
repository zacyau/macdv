import baostock as bs
import pandas as pd
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_cache: Dict[str, Any] = {}
_cache_ttl = 3600


def _cache_key(stock_code: str) -> str:
    return f"stock:{stock_code}"


def _get_cached(stock_code: str) -> Optional[Any]:
    key = _cache_key(stock_code)
    entry = _cache.get(key)
    if not entry:
        return None
    if time.time() - entry["ts"] > _cache_ttl:
        del _cache[key]
        return None
    return entry["data"]


def _set_cached(stock_code: str, data: Any):
    _cache[_cache_key(stock_code)] = {"ts": time.time(), "data": data}


_bs_logged_in = False


import threading

_bs_lock = threading.Lock()

def _ensure_login_bs():
    global _bs_logged_in
    with _bs_lock:
        if not _bs_logged_in:
            lg = bs.login()
            if lg.error_code != "0":
                logger.error(f"baostock login failed: {lg.error_msg}")
                raise ConnectionError(f"baostock login failed: {lg.error_msg}")
            _bs_logged_in = True


def _logout_bs():
    global _bs_logged_in
    with _bs_lock:
        if _bs_logged_in:
            bs.logout()
            _bs_logged_in = False


def _resolve_code(stock_code: Optional[str], stock_name: Optional[str]) -> str:
    if stock_code:
        code = stock_code.strip()
        if not code.startswith(("sh.", "sz.", "bj.")):
            if code.startswith("6"):
                code = f"sh.{code}"
            elif code.startswith(("0", "3")):
                code = f"sz.{code}"
            elif code.startswith(("4", "8")):
                code = f"bj.{code}"
            else:
                # try sh first, then sz
                for prefix in ("sh.", "sz."):
                    try:
                        _ensure_login_bs()
                        rs = bs.query_stock_basic(code=f"{prefix}{code}")
                        if rs.error_code == "0" and rs.next():
                            return f"{prefix}{code}"
                    finally:
                        _logout_bs()
                raise ValueError(f"cannot resolve stock code: {stock_code}")
        return code

    if stock_name:
        _ensure_login_bs()
        try:
            rs = bs.query_stock_basic(code="", code_name=stock_name.strip())
            data = []
            while rs.error_code == "0" and rs.next():
                data.append(rs.get_row_data())
            if not data:
                raise ValueError(f"no stock found with name: {stock_name}")
            for row in data:
                if row[4] in ("1", "5"):
                    return row[0]
            raise ValueError(f"no valid stock/ETF found with name: {stock_name}")
        finally:
            _logout_bs()
    raise ValueError("stock_code or stock_name is required")


def _query_name_by_code(stock_code: str) -> str:
    _ensure_login_bs()
    try:
        rs = bs.query_stock_basic(code=stock_code)
        if rs.error_code == "0" and rs.next():
            return rs.get_row_data()[1]
    finally:
        _logout_bs()
    return stock_code


def fetch_stock_data(stock_code: Optional[str] = None, stock_name: Optional[str] = None) -> Dict[str, Any]:
    code = _resolve_code(stock_code, stock_name)
    cached = _get_cached(code)
    if cached:
        return cached

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")

    _ensure_login_bs()
    try:
        rs = bs.query_history_k_data_plus(
            code,
            "date,code,open,high,low,close,volume,amount,turn,pctChg",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3"
        )

        data_list = []
        while rs.error_code == "0" and rs.next():
            data_list.append(rs.get_row_data())

        if not data_list:
            raise ValueError(f"no data found for {code}")

        df = pd.DataFrame(data_list, columns=rs.fields)
        for col in ["open", "high", "low", "close", "volume", "amount", "turn", "pctChg"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df.dropna(subset=["close"])
        if df.empty:
            raise ValueError(f"no valid data for {code}")
    finally:
        _logout_bs()

    name = _query_name_by_code(code)
    latest = df.iloc[-1]
    result = {
        "stock_name": name,
        "stock_code": code.split(".")[-1],
        "trade_date": str(latest["date"]),
        "current_price": float(latest["close"]),
        "df": df
    }
    _set_cached(code, result)
    return result
