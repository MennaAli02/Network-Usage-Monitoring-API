# model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Line(Base):
    __tablename__ = "lines"

    id = Column(Integer, primary_key=True, index=True)
    line_number = Column(String, unique=True, index=True)
    name = Column(String, unique=True, index=True)

    def __repr__(self):
        return f"<Line(id={self.id}, line_number='{self.line_number}', name='{self.name}')>"


class QuotaResults(Base):
    __tablename__ = "quota_results"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(String, unique=True, index=True)
    line_id = Column(Integer, ForeignKey("lines.id"), index=True)
    data_used = Column(Integer, index=True)
    usage_percentage = Column(Integer, index=True)
    data_remaining = Column(Integer, index=True)
    balance = Column(Integer, index=True)
    renewal_date = Column(String, index=True)
    remaining_days = Column(Integer, index=True)
    renewal_cost = Column(Integer, index=True)
    date_time = Column(DateTime, index=True)

    def __repr__(self):
        return (
            f"<quota_results(id={self.id}, process_id='{self.process_id}', "
            f"line_id={self.line_id}, data_used={self.data_used}, "
            f"usage_percentage={self.usage_percentage}, "
            f"data_remaining={self.data_remaining}, balance={self.balance}, "
            f"renewal_date='{self.renewal_date}', remaining_days={self.remaining_days}, "
            f"renewal_cost={self.renewal_cost}, date_time={self.date_time})>"
        )


class SpeedTestResult(Base):
    __tablename__ = "speed_test_results"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(String, unique=True, index=True)
    line_id = Column(Integer, ForeignKey("lines.id"), index=True)
    ping = Column(Integer, index=True)
    upload_speed = Column(Integer, index=True)
    download_speed = Column(Integer, index=True)
    public_ip = Column(String, index=True)
    date_time = Column(DateTime, index=True)

    def __repr__(self):
        return (
            f"<speed_test_results(id={self.id}, process_id='{self.process_id}', "
            f"line_id={self.line_id}, ping={self.ping}, upload_speed={self.upload_speed}, "
            f"download_speed={self.download_speed}, public_ip='{self.public_ip}', "
            f"date_time={self.date_time})>"
        )
