from weatherDataCollector import WeatherDataCollector
import datetime


class UserInterface:
    def __init__(self, data_collector):
        self.weather_collector = data_collector
        self.action = 0
        self.action_range = range(1, 6)

    def validate_date(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            print("Incorrect data format, should be YYYY-MM-DD")
            return False

    def validate_hour(self, hour):
        try:
            if int(hour) > 24 or int(hour) < 1:
                print("hour must be a number between 1-24")
                return False
            else:
                return True
        except ValueError:
            print("hour must be a number between 1-24")
            return False

    def input_ids(self):
        devices_start_id = ""
        devices_end_id = ""
        while not devices_start_id.isnumeric() or not devices_end_id.isnumeric():
            print("to get data from one device enter same first and last id")
            devices_start_id = input("input first id: ")
            devices_end_id = input("input last id: ")

            if not devices_start_id.isnumeric() or not devices_end_id.isnumeric():
                print("both ids must be a number")

        return devices_start_id, devices_end_id

    def input_dates(self):
        start_date = ""
        end_date = ""
        proper_user_info = False
        while not proper_user_info:
            start_date = input("enter beginning date in format YYYY-MM-DD: ")
            proper_user_info = self.validate_date(start_date)
            if not proper_user_info:
                continue

            start_hour = str(input("enter beginning hour: "))
            proper_user_info = self.validate_hour(start_hour)
            if not proper_user_info:
                continue

            end_date = input("enter ending date in format YYYY-MM-DD: ")
            proper_user_info = self.validate_date(end_date)
            if not proper_user_info:
                continue

            end_hour = str(input("enter ending hour: "))
            proper_user_info = self.validate_hour(end_hour)
            if not proper_user_info:
                continue

            start_date = start_date + '-' + start_hour
            end_date = end_date + '-' + end_hour

        return start_date, end_date

    def get_all_recent_data(self):
        weather_data = self.weather_collector.get_all_recent_data()
        if weather_data == -1:
            print("Cannot receive data from server")
            return

        for measurement in weather_data['measurements']:
            print(measurement)

    def get_data_from_id_range(self):
        devices_start_id, devices_end_id = self.input_ids()
        weather_data = self.weather_collector.get_data_from_id_range(devices_start_id, devices_end_id)
        if weather_data == -1:
            print("Cannot receive data from server")
            return

        for measurement in weather_data['measurements']:
            print(measurement)

    def get_data_from_date_range(self):
        start_date, end_date = self.input_dates()
        weather_data = self.weather_collector.get_data_from_date_range(start_date, end_date)
        if weather_data == -1:
            print("Cannot receive data from server")
            return

        for measurement in weather_data['measurements']:
            print(measurement)

    def get_data_from_id_date_range(self):
        devices_start_id, devices_end_id = self.input_ids()
        start_date, end_date = self.input_dates()
        weather_data = self.weather_collector.get_data_from_id_date_range(devices_start_id, devices_end_id, start_date, end_date)
        if weather_data == -1:
            print("Cannot receive data from server")
            return

        for measurement in weather_data['measurements']:
            print(measurement)

    def execute_action(self):
        if self.action == 1:
            self.get_all_recent_data()
        elif self.action == 2:
            self.get_data_from_id_range()
        elif self.action == 3:
            self.get_data_from_date_range()
        elif self.action == 4:
            self.get_data_from_id_date_range()
        elif self.action == 5:
            print("bye!")

    def start(self):
        while self.action != 5:
            print("\nWhat would you like to do:")
            print("1 - get all last reads")
            print("2 - get data from particular device or range of devices")
            print("3 - get data from particular range of time")
            print("4 - get data from range of devices and range of time")
            print("5 - exit the application")
            try:
                self.action = int(input("choose one option: "))
            except ValueError:
                print("value must be a number\n")
                continue

            if self.action not in self.action_range:
                print("please enter number between 1-5\n")
                continue

            self.execute_action()


if __name__ == "__main__":
    weather_collector = WeatherDataCollector("https://127.0.0.1:5000/server")
    interface = UserInterface(weather_collector)

    interface.start()
