from pydantic import BaseModel
from typing import Optional


class StockQueryResponse(BaseModel):
    stock_name: str
    stock_code: str
    trade_date: str
    current_price: float
    macdv: float
    rsi14: float
    macdv_trend: str
    rsi14_signal: str
    updated_at: str


class StockQueryRequest(BaseModel):
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
