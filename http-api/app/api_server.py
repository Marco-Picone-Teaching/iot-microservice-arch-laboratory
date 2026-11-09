from flask import Flask
from flask_restful import Api
from persistence.data_manager import DataManager
from resources.telemetry_data_resource import TelemetryDataResource
import yaml

# Default Values
CONF_FILE_PATH = "conf.yaml"
DEFAULT_ENDPOINT_PREFIX = "/api/v1/iot/inventory"

# Default Configuration Dictionary
configuration_dict = {
    "rest":{
        "api_prefix": DEFAULT_ENDPOINT_PREFIX, 
        "host": "0.0.0.0",
        "port": 7070
    }
}

# Read Configuration from target Configuration File Path
def read_configuration_file():
    global configuration_dict

    with open(CONF_FILE_PATH, 'r') as file:
        configuration_dict = yaml.safe_load(file)

    return configuration_dict

# Read Configuration file
configuration_dict = read_configuration_file()

print("Read Configuration from file ({}): {}".format(CONF_FILE_PATH, configuration_dict))

app = Flask(__name__)
api = Api(app)

print("Starting HTTP RESTful API Server ...")

data_manager = DataManager()

# Add Resources and Endpoints
api.add_resource(TelemetryDataResource, configuration_dict['rest']['api_prefix'] + '/device/<string:device_id>/telemetry',
                      resource_class_kwargs={'data_manager': data_manager},
                      endpoint="device_telemetry_data",
                      methods=['GET', 'POST'])

if __name__ == '__main__':

    # Run the Flask Application
    app.run(host=configuration_dict['rest']['host'], port=configuration_dict['rest']['port'])  # run our Flask app