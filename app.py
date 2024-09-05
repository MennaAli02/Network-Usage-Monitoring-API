from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from db.schema import (
    LineSchema,
    TotalDataUsedPerLine,
    RenewalCostCount,
    RemainingBalanceByLine,
    AverageSpeedsPerLine,
    AveragePingPerLine,
)
from db.crud import (
    read_lines,
    read_quota_results,
    read_speed_test_results,
    get_total_dataused_per_line,
    get_count_per_renewal_cost,
    remaining_balance_by_line,
    average_speeds_per_line,
    average_ping_per_line,
)
from db.database import get_db

app = FastAPI()


@app.get("/")
async def root():
    """
    Root endpoint to check service health.
    """
    return {"message": "Hello World"}


@app.get("/lines", response_model=List[LineSchema])
async def get_lines(id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Fetches all lines or a specific line by ID.
    """
    return read_lines(db, id)


@app.get("/quota-results")
async def get_quota_results(
    line_id: Optional[int] = None, db: Session = Depends(get_db)
):
    """
    Fetches quota results for a specific line.
    """
    return read_quota_results(db, line_id)


@app.get("/speed-test-results")
async def get_speed_test_results(
    line_id: Optional[int] = None, db: Session = Depends(get_db)
):
    """
    Fetches speed test results for a specific line.
    """
    return read_speed_test_results(db, line_id)


@app.get("/total-dataused-per-line", response_model=List[TotalDataUsedPerLine])
async def get_total_dataused_per_line(db: Session = Depends(get_db)):
    """
    Fetches total data usage for all lines.
    """
    return get_total_dataused_per_line(db)


@app.get("/count-per-renewal-cost", response_model=List[RenewalCostCount])
async def get_count_per_renewal_cost(db: Session = Depends(get_db)):
    """
    Fetches the count of occurrences for each renewal cost.
    """
    return get_count_per_renewal_cost(db)


@app.get("/remaining-balance-by-line", response_model=List[RemainingBalanceByLine])
async def get_remaining_balance_by_line(db: Session = Depends(get_db)):
    """
    Fetches the remaining balance for all lines.
    """
    return remaining_balance_by_line(db)


@app.get("/average-speeds-per-line", response_model=List[AverageSpeedsPerLine])
async def get_average_speeds_per_line(
    days: int = Query(
        ..., description="Number of days to calculate average speeds over"
    ),
    db: Session = Depends(get_db),
):
    """
    Fetches the average upload and download speeds for each line over a specified number of days.
    """
    return average_speeds_per_line(db, days=days)


@app.get("/average-ping-per-line", response_model=List[AveragePingPerLine])
async def get_average_ping_per_line(
    days: int = Query(..., description="Number of days to calculate average ping over"),
    db: Session = Depends(get_db),
):
    """
    Fetches the average ping for each line over a specified number of days.
    """
    return average_ping_per_line(db, days=days)
