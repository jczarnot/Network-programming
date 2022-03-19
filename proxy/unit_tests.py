
import unittest
from Proxy import *


class TestProxyAlghorithms(unittest.TestCase):

    def test_caching_data_with_amount_lesser_than_maximum_cached_data(self):
        sock = Socket(ip_version=4, HOST='127.0.0.1', port = 8000)
        proxy = Proxy(sock)

        data = {'measurements': [{'device_id' : 12, 'time' : 50, 'temperature' : 18, 'pressure' : 1000, 'humidity' : 50}, {'device_id' : 13, 'time' : 55, 'temperature' : 22, 'pressure' : 1000, 'humidity' : 67}, {'device_id' : 15, 'time' : 50, 'temperature' : 18, 'pressure' : 1000, 'humidity' : 50}, {'device_id' : 16, 'time' : 55, 'temperature' : 22, 'pressure' : 1000, 'humidity' : 67}]}

        proxy.cache_data(data)
        cached = proxy.cached_data

        self.assertEqual(cached, data)

    def test_if_caching_starts_with_empty_array(self):
        sock = Socket(ip_version=4, HOST='127.0.0.1', port = 8000)
        proxy = Proxy(sock)

        cached = proxy.cached_data

        self.assertEqual(cached, {'measurements': []})

    def test_caching_data_with_amount_greater_than_maximum_cached_data(self):
        sock = Socket(ip_version=4, HOST='127.0.0.1', port = 8000)
        proxy = Proxy(sock)

        data = {'measurements': [{'device_id' : 12, 'time' : 50, 'temperature' : 18, 'pressure' : 1000, 'humidity' : 50}, {'device_id' : 13, 'time' : 55, 'temperature' : 22, 'pressure' : 1000, 'humidity' : 67}, {'device_id' : 15, 'time' : 50, 'temperature' : 18, 'pressure' : 1000, 'humidity' : 50}, {'device_id' : 16, 'time' : 55, 'temperature' : 22, 'pressure' : 1000, 'humidity' : 67}, {'device_id' : 12, 'time' : 50, 'temperature' : 18, 'pressure' : 1000, 'humidity' : 50}, {'device_id' : 13, 'time' : 55, 'temperature' : 22, 'pressure' : 1000, 'humidity' : 67}, {'device_id' : 15, 'time' : 50, 'temperature' : 18, 'pressure' : 1000, 'humidity' : 50}, {'device_id' : 16, 'time' : 55, 'temperature' : 22, 'pressure' : 1000, 'humidity' : 67}]}

        data_fixed = {'measurements':[{'device_id' : 16, 'time' : 55, 'temperature' : 22, 'pressure' : 1000, 'humidity' : 67}]}

        files_names = proxy.cache_data(data)
        cached = proxy.cached_data

        if proxy.max_cached == 7:
            self.assertEqual(cached, data_fixed)

        else:
            self.assertNotEqual(cached, data_fixed)

        for file_name in files_names:
            os.remove(file_name) 


    def test_if_checking_single_measurement_return_proper_value_for_true(self):
        sock = Socket(ip_version=4, HOST='127.0.0.1', port = 8000)
        proxy = Proxy(sock)

        result = proxy._check_if_single_measurement_have_proper_value('device_id', 96)
        self.assertEqual(result, 1)

        result = proxy._check_if_single_measurement_have_proper_value('temperature', -25)
        self.assertEqual(result, 1)

        result = proxy._check_if_single_measurement_have_proper_value('time',  1642455603)
        self.assertEqual(result, 1)

        result = proxy._check_if_single_measurement_have_proper_value('pressure',  1024)
        self.assertEqual(result, 1)

        result = proxy._check_if_single_measurement_have_proper_value('humidity',  32)
        self.assertEqual(result, 1)

    def test_if_checking_single_measurement_return_proper_value_for_false(self):
        sock = Socket(ip_version=4, HOST='127.0.0.1', port = 8000)
        proxy = Proxy(sock)

        result = proxy._check_if_single_measurement_have_proper_value('device_id', 112)
        self.assertEqual(result, 0)

        result = proxy._check_if_single_measurement_have_proper_value('device_id', -17)
        self.assertEqual(result, 0)


        result = proxy._check_if_single_measurement_have_proper_value('temperature', -88)
        self.assertEqual(result, 0)

        result = proxy._check_if_single_measurement_have_proper_value('temperature', 125)
        self.assertEqual(result, 0)


        result = proxy._check_if_single_measurement_have_proper_value('time',  3642854871)
        self.assertEqual(result, 0)

        result = proxy._check_if_single_measurement_have_proper_value('time',  1622054871)
        self.assertEqual(result, 0)

        result = proxy._check_if_single_measurement_have_proper_value('time',  -1054871)
        self.assertEqual(result, 0)


        result = proxy._check_if_single_measurement_have_proper_value('pressure',  1199)
        self.assertEqual(result, 0)

        result = proxy._check_if_single_measurement_have_proper_value('pressure',  860)
        self.assertEqual(result, 0)

        result = proxy._check_if_single_measurement_have_proper_value('pressure',  -411)
        self.assertEqual(result, 0)


        result = proxy._check_if_single_measurement_have_proper_value('humidity',  114)
        self.assertEqual(result, 0)

        result = proxy._check_if_single_measurement_have_proper_value('humidity',  -8)
        self.assertEqual(result, 0)

    def test_if_checking_multiple_measurement_return_proper_value_for_true(self):
        sock = Socket(ip_version=4, HOST='127.0.0.1', port = 8000)
        proxy = Proxy(sock)

        data = {'measurements': [{'device_id' : 12, 'time' : 1642455603, 'temperature' : 18, 'pressure' : 1000, 'humidity' : 50}, {'device_id' : 13, 'time' : 1642455603, 'temperature' : 22, 'pressure' : 1000, 'humidity' : 67}, {'device_id' : 15, 'time' : 1642454871, 'temperature' : 18, 'pressure' : 1000, 'humidity' : 50}, {'device_id' : 36, 'time' : 1642454871, 'temperature' : 22, 'pressure' : 1000, 'humidity' : 67}]}

        result = proxy.check_if_data_have_proper_values(data)

        self.assertEqual(result, 1)

    def test_if_checking_multiple_measurement_return_proper_value_for_false(self):
        sock = Socket(ip_version=4, HOST='127.0.0.1', port = 8000)
        proxy = Proxy(sock)

        data = {'measurements': [{'device_id' : 12, 'time' : 1642455603, 'temperature' : 18, 'pressure' : 1000, 'humidity' : 50}, {'device_id' : 13, 'time' : 1642455603, 'temperature' : 22, 'pressure' : 1000, 'humidity' : 67}, {'device_id' : 15, 'time' : 1642455603, 'temperature' : 18, 'pressure' : 1000, 'humidity' : 50}, {'device_id' : 16, 'time' : 55, 'temperature' : 22, 'pressure' : 1000, 'humidity' : 67}]}

        result = proxy.check_if_data_have_proper_values(data)

        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()