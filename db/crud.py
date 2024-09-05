import logging
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from db.model import Line, QuotaResults, SpeedTestResult
from db.schema import (
    LineSchema,
    QuotaResultSchema,
    SpeedTestResultSchema,
    AverageSpeedsPerLine,
    AveragePingPerLine,
)
from typing import List
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def read_lines(session: Session, id: int = None):
    """
    Fetches lines from the database. Optionally filters by line ID.

    Args:
        session (Session): SQLAlchemy session for database interaction.
        id (int, optional): The ID of the line to filter by. Defaults to None.

    Returns:
        List[LineSchema]: List of validated line records.
    """
    stmt = select(Line)

    if id:
        stmt = stmt.where(Line.id == id)

    results = session.execute(stmt).scalars().all()
    logger.info(f"Fetched {len(results)} lines from the database.")
    return [LineSchema.model_validate(line) for line in results]


def read_quota_results(session: Session, line_id: int = None):
    """
    Fetches quota results from the database. Optionally filters by line ID.

    Args:
        session (Session): SQLAlchemy session for database interaction.
        line_id (int, optional): The ID of the line to filter by. Defaults to None.

    Returns:
        List[QuotaResultSchema]: List of validated quota result records.
    """
    stmt = select(QuotaResults)
    if line_id:
        stmt = stmt.where(QuotaResults.line_id == line_id)
    stmt = stmt.order_by(desc(QuotaResults.date_time))

    results = session.execute(stmt).scalars().all()
    logger.info(f"Fetched {len(results)} quota results from the database.")
    return [QuotaResultSchema.model_validate(result) for result in results]


def read_speed_test_results(session: Session, line_id: int = None):
    """
    Fetches speed test results from the database. Optionally filters by line ID.

    Args:
        session (Session): SQLAlchemy session for database interaction.
        line_id (int, optional): The ID of the line to filter by. Defaults to None.

    Returns:
        List[SpeedTestResultSchema]: List of validated speed test result records.
    """
    stmt = select(SpeedTestResult)
    if line_id:
        stmt = stmt.where(SpeedTestResult.line_id == line_id)

    results = session.execute(stmt).scalars().all()
    logger.info(f"Fetched {len(results)} speed test results from the database.")
    return [SpeedTestResultSchema.model_validate(result) for result in results]


def get_total_dataused_per_line(session: Session):
    """
    Fetches total data used per line and displays it as a bar chart.

    Args:
        session (Session): SQLAlchemy session for database interaction.
    """
    stmt = select(
        QuotaResults.line_id,
        func.sum(QuotaResults.data_used).label("total_dataused"),
    ).group_by(QuotaResults.line_id)

    results = session.execute(stmt).fetchall()
    logger.info(f"Fetched total data usage for {len(results)} lines.")

    line_ids = [result.line_id for result in results]
    total_dataused = [result.total_dataused for result in results]

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.bar(line_ids, total_dataused, color="skyblue")
    plt.xlabel("Line ID")
    plt.ylabel("Total Data Used")
    plt.title("Total Data Used per Line ID")
    plt.xticks(line_ids)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()
    logger.info("Displayed total data used per line chart.")


def get_count_per_renewal_cost(session: Session):
    """
    Fetches the count of occurrences for each renewal cost and displays it as a pie chart.

    Args:
        session (Session): SQLAlchemy session for database interaction.
    """
    stmt = (
        session.query(QuotaResults.renewal_cost, func.count().label("count"))
        .filter(QuotaResults.renewal_cost.isnot(None))
        .group_by(QuotaResults.renewal_cost)
        .all()
    )
    logger.info(f"Fetched renewal cost counts for {len(stmt)} renewal cost categories.")

    renewal_costs = [float(row.renewal_cost) for row in stmt]
    counts = [row.count for row in stmt]

    # Plot the data
    plt.figure(figsize=(8, 8))
    plt.pie(
        counts,
        labels=[f"{cost:.2f}" for cost in renewal_costs],
        autopct="%1.1f%%",
        colors=plt.cm.Paired(range(len(counts))),
    )
    plt.title("Distribution of Counts by Renewal Cost")
    plt.show()
    logger.info("Displayed pie chart for renewal cost distribution.")


def remaining_balance_by_line(session: Session):
    """
    Fetches and logs the total remaining balance by line.

    Args:
        session (Session): SQLAlchemy session for database interaction.
    """
    results = (
        session.query(
            QuotaResults.line_id,
            func.sum(QuotaResults.balance).label("total_balance"),
        )
        .group_by(QuotaResults.line_id)
        .all()
    )
    logger.info(f"Fetched remaining balances for {len(results)} lines.")

    for result in results:
        logger.info(
            f"Line ID: {result.line_id}, Total Remaining Balance: {result.total_balance}"
        )


def average_speeds_per_line(session: Session, days: int) -> List[AverageSpeedsPerLine]:
    """
    Fetches the average upload and download speeds per line over a specified period.

    Args:
        session (Session): SQLAlchemy session for database interaction.
        days (int): The number of days in the past to consider.

    Returns:
        List[AverageSpeedsPerLine]: List of average upload and download speeds per line.
    """
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    stmt = (
        select(
            SpeedTestResult.line_id,
            func.avg(SpeedTestResult.upload_speed).label("avg_upload_speed"),
            func.avg(SpeedTestResult.download_speed).label("avg_download_speed"),
        )
        .filter(SpeedTestResult.date_time.between(start_date, end_date))
        .group_by(SpeedTestResult.line_id)
    )

    results = session.execute(stmt).fetchall()
    logger.info(f"Fetched average speeds for {len(results)} lines over {days} days.")
    return [AverageSpeedsPerLine.model_validate(row) for row in results]


def average_ping_per_line(session: Session, days: int) -> List[AveragePingPerLine]:
    """
    Fetches the average ping per line over a specified period.

    Args:
        session (Session): SQLAlchemy session for database interaction.
        days (int): The number of days in the past to consider.

    Returns:
        List[AveragePingPerLine]: List of average ping values per line.
    """
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    stmt = (
        select(
            SpeedTestResult.line_id, func.avg(SpeedTestResult.ping).label("avg_ping")
        )
        .filter(SpeedTestResult.date_time.between(start_date, end_date))
        .group_by(SpeedTestResult.line_id)
    )

    results = session.execute(stmt).all()
    logger.info(f"Fetched average ping for {len(results)} lines over {days} days.")
    return [AveragePingPerLine.model_validate(row) for row in results]
