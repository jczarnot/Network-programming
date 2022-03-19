from database import Database
import datetime
from flask import Flask
from flask_restful import Resource, Api, reqparse
from werkzeug.exceptions import BadRequest
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


USER_DATA = {
    "server" : "pass"
}

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

parser = reqparse.RequestParser()
parser.add_argument('measurements', type=dict, action='append')

server_cache = ""


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


class WeatherData(Resource):
    def __init__(self):
        self.database = Database("postgres", "postgres", "admin")

    def separate_ids(self, devices_id):
        id_range = devices_id.split(':')
        start_id = int(id_range[0])
        end_id = int(id_range[1])
        return start_id, end_id

    def separate_dates(self, date_range):
        date_range = date_range.split(':')
        start_date = date_range[0]
        end_date = date_range[1]
        start_date = [int(d) for d in start_date.split('-')]
        end_date = [int(d) for d in end_date.split('-')]

        start_time = datetime.datetime(start_date[0], start_date[1], start_date[2], start_date[3])
        start_time = int((start_time - datetime.datetime(1970, 1, 1)).total_seconds())
        end_time = datetime.datetime(end_date[0], end_date[1], end_date[2], end_date[3])
        end_time = int((end_time - datetime.datetime(1970, 1, 1)).total_seconds())

        return start_time, end_time

    def get_data_from_id_range(self, devices_id):
        start_id, end_id = self.separate_ids(devices_id)
        return self.database.get_measurements_for_id(start_id, end_id)

    def get_data_from_date_range(self, date_range):
        start_time, end_time = self.separate_dates(date_range)
        return self.database.get_measurements_for_date(start_time, end_time)

    def get_data_from_id_date_range(self, devices_id, date_range):
        start_id, end_id = self.separate_ids(devices_id)
        start_time, end_time = self.separate_dates(date_range)
        return self.database.get_measurements_for_id_date(start_id, end_id, start_time, end_time)

    def get(self, devices_id, date_range):
        global server_cache

        try:
            # get all recent data
            if devices_id == '0' and date_range == '0':
                return server_cache
            # get data from id range
            elif date_range == '0':
                self.database.open_connection()
                data = self.get_data_from_id_range(devices_id)
                self.database.close_connection()
                return data
            # get data from date range
            elif devices_id == '0':
                self.database.open_connection()
                data = self.get_data_from_date_range(date_range)
                self.database.close_connection()
                return data
            # get data from id and date range
            else:
                self.database.open_connection()
                data = self.get_data_from_id_date_range(devices_id, date_range)
                self.database.close_connection()
                return data
        except ValueError:
            self.database.close_connection()
            raise BadRequest('wrong request')


class Server(Resource):
    def __init__(self):
        self.database = Database("postgres", "postgres", "admin")

    def get(self):
        return "server test"

    @auth.login_required
    def post(self):
        data = parser.parse_args()
        global server_cache
        server_cache = data
        self.database.open_connection()
        self.database.save_measurements(data)
        self.database.close_connection()
        return parser.parse_args()


api.add_resource(Server, '/server')
api.add_resource(WeatherData, '/server/<devices_id>/<date_range>')

# context = ('server.crt', 'server.key')
if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
    # app.run(debug=True)
