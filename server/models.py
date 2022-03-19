from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float

Base = declarative_base()


class Measurements(Base):
    __tablename__ = 'measurements'
    device_id = Column(Integer, primary_key=True)
    time = Column(Integer, primary_key=True)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)

    def __repr__(self):
        return "<Measurement(device_id='{}', time='{}', temperature={}, pressure={}, humidity={})>" \
            .format(self.device_id, self.time, self.temperature, self.pressure, self.humidity)