import json
from typing import Dict
import Proxy


def read(path_to_file: str) -> Dict:
    with open(path_to_file) as f:
        return json.loads(f.read())


def load_configuration(path_to_file: str, object: Proxy.Proxy) -> None:
    configuration = read(path_to_file)
    object.server_url = configuration['server_url']
    object.max_cached = configuration['max_cached']
    object.proper_measurements_values = configuration['proper_measurements_values']
    object.proper_ips = configuration['proper_ips']
    object.device_ids = configuration['device_ids']
