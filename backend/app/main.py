import time
import logging
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.models import StockQueryResponse
from app.data_service import fetch_stock_data
from app.indicators import get_latest_indicators

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Stock Analysis API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_rate_limit_store: dict = {}
_rate_limit_window = 60
_rate_limit_max = 5


def _check_rate_limit(client_ip: str) -> bool:
    now = time.time()
    window = _rate_limit_store.get(client_ip, [])
    window = [t for t in window if now - t < _rate_limit_window]
    if len(window) >= _rate_limit_max:
        return False
    window.append(now)
    _rate_limit_store[client_ip] = window
    return True


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(ConnectionError)
async def connection_error_handler(request: Request, exc: ConnectionError):
    return JSONResponse(status_code=503, content={"detail": str(exc)})


@app.get("/api/stock/query", response_model=StockQueryResponse)
async def query_stock(
    request: Request,
    stock_code: Optional[str] = Query(None),
    stock_name: Optional[str] = Query(None)
):
    client_ip = request.client.host if request.client else "unknown"
    if not _check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="rate limit exceeded: max 5 requests per minute")

    if not stock_code and not stock_name:
        raise HTTPException(status_code=422, detail="stock_code or stock_name is required")

    try:
        data = fetch_stock_data(stock_code=stock_code, stock_name=stock_name)
    except ValueError as e:
        logger.warning(f"query failed for code={stock_code} name={stock_name}: {e}")
        raise
    except Exception as e:
        logger.error(f"unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"internal server error: {str(e)}")

    indicators = get_latest_indicators(data["df"])

    return StockQueryResponse(
        stock_name=data["stock_name"],
        stock_code=data["stock_code"],
        trade_date=data["trade_date"],
        current_price=data["current_price"],
        macdv=indicators["macdv"],
        rsi14=indicators["rsi14"],
        macdv_trend=indicators["macdv_trend"],
        rsi14_signal=indicators["rsi14_signal"],
        updated_at=datetime.now().isoformat()
    )
