from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class LineSchema(BaseModel):
    id: int
    line_number: str
    name: str

    class Config:
        from_attributes = True


class QuotaResultSchema(BaseModel):
    id: Optional[int] = None
    process_id: Optional[str] = None
    line_id: Optional[int] = None
    data_used: Optional[int] = None
    usage_percentage: Optional[int] = None
    data_remaining: Optional[int] = None
    balance: Optional[int] = None
    renewal_date: Optional[str] = None
    remaining_days: Optional[int] = None
    renewal_cost: Optional[int] = None
    date_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class SpeedTestResultSchema(BaseModel):
    id: int
    process_id: str
    line_id: int
    ping: int
    upload_speed: int
    download_speed: int
    public_ip: str
    date_time: datetime

    class Config:
        from_attributes = True


class TotalDataUsedPerLine(BaseModel):
    line_id: int
    total_dataused: float


class RenewalCostCount(BaseModel):
    renewal_cost: float
    count: int


class RemainingBalanceByLine(BaseModel):
    line_id: int
    total_balance: float


class AverageSpeedsPerLine(BaseModel):
    line_id: Optional[int]
    avg_upload_speed: Optional[float]
    avg_download_speed: Optional[float]

    class Config:
        from_attributes = True


class AveragePingPerLine(BaseModel):
    line_id: Optional[int]
    avg_ping: Optional[float]

    class Config:
        from_attributes = True
