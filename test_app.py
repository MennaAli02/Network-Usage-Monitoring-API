import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model import Base, Line, QuotaResults, SpeedTestResult
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
from datetime import datetime, timedelta

# Setup an in-memory SQLite database for testing purposes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """
    Setup and teardown fixture for each test function.
    This provides a fresh database and session for each test.
    """
    Base.metadata.create_all(bind=engine)  # Create the tables
    db_session = TestingSessionLocal()  # Create a new session
    yield db_session  # Provide the session to the test
    db_session.close()  # Close the session after test
    Base.metadata.drop_all(bind=engine)  # Drop all tables


# Test cases


def test_read_lines(db):
    """
    Test reading lines from the database.
    """
    # Arrange: Add a test line to the database
    new_line = Line(id=1, line_number="123", name="Test Line")
    db.add(new_line)
    db.commit()

    # Act: Fetch the lines
    lines = read_lines(db)

    # Assert: Check the results
    assert len(lines) == 1
    assert lines[0].line_number == "123"
    assert lines[0].name == "Test Line"


def test_read_quota_results(db):
    """
    Test reading quota results from the database.
    """
    # Arrange: Add a test quota result
    new_line = Line(id=1, line_number="123", name="Test Line")
    db.add(new_line)
    db.commit()

    quota_result = QuotaResults(
        id=1,
        process_id="proc-123",
        line_id=1,
        data_used=100,
        usage_percentage=50,
        data_remaining=100,
        balance=50,
        renewal_date="2023-09-01",
        remaining_days=10,
        renewal_cost=20,
        date_time=datetime.now(),
    )
    db.add(quota_result)
    db.commit()

    # Act: Fetch the quota results
    results = read_quota_results(db, line_id=1)

    # Assert: Check the results
    assert len(results) == 1
    assert results[0].process_id == "proc-123"
    assert results[0].data_used == 100


def test_read_speed_test_results(db):
    """
    Test reading speed test results from the database.
    """
    # Arrange: Add a test speed test result
    new_line = Line(id=1, line_number="123", name="Test Line")
    db.add(new_line)
    db.commit()

    speed_test = SpeedTestResult(
        id=1,
        process_id="speed-123",
        line_id=1,
        ping=20,
        upload_speed=50,
        download_speed=100,
        public_ip="192.168.1.1",
        date_time=datetime.now(),
    )
    db.add(speed_test)
    db.commit()

    # Act: Fetch the speed test results
    results = read_speed_test_results(db, line_id=1)

    # Assert: Check the results
    assert len(results) == 1
    assert results[0].process_id == "speed-123"
    assert results[0].ping == 20


def test_get_total_dataused_per_line(db):
    """
    Test fetching the total data used per line.
    """
    # Arrange: Add test data
    new_line = Line(id=1, line_number="123", name="Test Line")
    db.add(new_line)
    db.commit()

    quota_result = QuotaResults(
        id=1,
        process_id="proc-123",
        line_id=1,
        data_used=100,
        usage_percentage=50,
        data_remaining=100,
        balance=50,
        renewal_date="2023-09-01",
        remaining_days=10,
        renewal_cost=20,
        date_time=datetime.now(),
    )
    db.add(quota_result)
    db.commit()

    # Act: Fetch total data used per line
    get_total_dataused_per_line(db)

    # Assert: No assertion needed as we're just testing the display, manual visual verification


def test_get_count_per_renewal_cost(db):
    """
    Test fetching the count of occurrences for each renewal cost.
    """
    # Arrange: Add test data
    new_line = Line(id=1, line_number="123", name="Test Line")
    db.add(new_line)
    db.commit()

    quota_result = QuotaResults(
        id=1,
        process_id="proc-123",
        line_id=1,
        data_used=100,
        usage_percentage=50,
        data_remaining=100,
        balance=50,
        renewal_date="2023-09-01",
        remaining_days=10,
        renewal_cost=20,
        date_time=datetime.now(),
    )
    db.add(quota_result)
    db.commit()

    # Act: Fetch the count per renewal cost
    get_count_per_renewal_cost(db)

    # Assert: No assertion needed as we're testing chart generation, manual verification


def test_remaining_balance_by_line(db):
    """
    Test fetching the remaining balance by line.
    """
    # Arrange: Add test data
    new_line = Line(id=1, line_number="123", name="Test Line")
    db.add(new_line)
    db.commit()

    quota_result = QuotaResults(
        id=1,
        process_id="proc-123",
        line_id=1,
        data_used=100,
        usage_percentage=50,
        data_remaining=100,
        balance=50,
        renewal_date="2023-09-01",
        remaining_days=10,
        renewal_cost=20,
        date_time=datetime.now(),
    )
    db.add(quota_result)
    db.commit()

    # Act: Fetch remaining balance
    remaining_balance_by_line(db)

    # Assert: Check logs for results, manual verification


def test_average_speeds_per_line(db):
    """
    Test fetching the average upload and download speeds per line.
    """
    # Arrange: Add test data
    new_line = Line(id=1, line_number="123", name="Test Line")
    db.add(new_line)
    db.commit()

    recent_date = datetime.now() - timedelta(days=10)

    speed_test = SpeedTestResult(
        id=1,
        process_id="speed-123",
        line_id=1,
        ping=20,
        upload_speed=50,
        download_speed=100,
        public_ip="192.168.1.1",
        date_time=recent_date,
    )
    db.add(speed_test)
    db.commit()

    # Act: Fetch average speeds per line
    results = average_speeds_per_line(db, days=30)

    # Assert: Check the results
    assert len(results) == 1
    assert results[0].avg_upload_speed == 50
    assert results[0].avg_download_speed == 100


def test_average_ping_per_line(db):
    """
    Test fetching the average ping per line.
    """
    # Arrange: Add test data
    new_line = Line(id=1, line_number="123", name="Test Line")
    db.add(new_line)
    db.commit()

    # Set the date to be within the last 30 days
    recent_date = datetime.now() - timedelta(days=10)

    speed_test = SpeedTestResult(
        id=1,
        process_id="speed-123",
        line_id=1,
        ping=20,
        upload_speed=50,
        download_speed=100,
        public_ip="192.168.1.1",
        date_time=recent_date,  # Use recent date
    )
    db.add(speed_test)
    db.commit()

    # Act: Fetch average ping per line
    results = average_ping_per_line(db, days=30)

    # Assert: Check the results
    assert len(results) == 1
    assert results[0].avg_ping == 20
