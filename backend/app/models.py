from pydantic import BaseModel
from typing import Optional, List


class StockQueryResponse(BaseModel):
    stock_name: str
    stock_code: str
    trade_date: str
    current_price: float
    macdv: float
    rsi14: float
    macdv_trend: str
    rsi14_signal: str
    recommendation: Optional[str] = None
    updated_at: str


class StockQueryRequest(BaseModel):
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None


class BatchQueryRequest(BaseModel):
    queries: List[str]


class BatchQueryItem(BaseModel):
    stock_name: str
    stock_code: str
    trade_date: str
    current_price: float
    macdv: float
    rsi14: float
    macdv_trend: str
    rsi14_signal: str
    recommendation: Optional[str] = None
    error: Optional[str] = None


class BatchQueryResponse(BaseModel):
    results: List[BatchQueryItem]
    updated_at: str
