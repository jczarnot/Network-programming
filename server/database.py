import models
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_


class Database:
    def __init__(self, name, user, password):
        try:
            self.engine = create_engine("postgresql+psycopg2://" + user + ":" + password + "@localhost:5432/" + name, echo=True)
        except(Exception, exc.SQLAlchemyError) as error:
            print(error)

    def open_connection(self):
        try:
            self.db = scoped_session(sessionmaker(bind=self.engine))
        except(Exception, exc.SQLAlchemyError) as error:
            print(error)

    def close_connection(self):
        if self.db is not None:
            self.db.close()

    def save_measurements(self, measurements):
        try:
            for m in measurements['measurements']:
                measurement = models.Measurements(device_id=m['device_id'], time=m['time'],
                                                  temperature=m['temperature'], pressure=m['pressure'],
                                                  humidity=m['humidity'])
                self.db.add(measurement)
            self.db.commit()
        except (Exception, exc.SQLAlchemyError) as error:
            print("Failed to insert record into measurements table", error)

    def get_measurements_for_id(self, start_id, end_id):
        try:
            measurements = {"measurements": []}
            result = self.db.query(models.Measurements).filter(
                        and_(models.Measurements.device_id >= start_id, models.Measurements.device_id <= end_id))
            for row in result:
                measurements["measurements"].append({"device_id": row.device_id, "time": row.time,
                                                     "temperature": row.temperature, "pressure": row.pressure,
                                                     "humidity": row.humidity})

            return measurements
        except (Exception, exc.SQLAlchemyError) as error:
            print("Failed to read data from database", error)

    def get_measurements_for_date(self, start_time, end_time):
        try:
            measurements = {"measurements": []}
            result = self.db.query(models.Measurements).filter(
                       and_(models.Measurements.time >= start_time, models.Measurements.time <= end_time))
            for row in result:
                measurements["measurements"].append({"device_id": row.device_id, "time": row.time,
                                                     "temperature": row.temperature, "pressure": row.pressure,
                                                     "humidity": row.humidity})

            return measurements
        except (Exception, exc.SQLAlchemyError) as error:
            print("Failed to read data from database", error)

    def get_measurements_for_id_date(self, start_id, end_id, start_time, end_time):
        try:
            measurements = {"measurements": []}
            result = self.db.query(models.Measurements).filter(
                and_(models.Measurements.device_id >= start_id, models.Measurements.device_id <= end_id,
                     models.Measurements.time >= start_time, models.Measurements.time <= end_time))
            for row in result:
                measurements["measurements"].append({"device_id": row.device_id, "time": row.time,
                                                     "temperature": row.temperature, "pressure": row.pressure,
                                                     "humidity": row.humidity})

            return measurements
        except (Exception, exc.SQLAlchemyError) as error:
            print("Failed to read data from database", error)