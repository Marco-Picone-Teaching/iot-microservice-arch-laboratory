from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource

class TelemetryDataResource(Resource):
    """Resource to handle the Telemetry Data of a specific Device"""

    def __init__(self, **kwargs):
        # Inject the DataManager instance
        self.data_manager = kwargs['data_manager']

    def get(self, device_id):
        """GET Request to retrieve the Telemetry Data of a target device"""

        device_telemetry_data = self.data_manager.get_telemetry_data_by_device_id(device_id)

        if device_telemetry_data is not None:
            result_location_list = []

            # Iterate over the telemetry data to build a serializable telemetry data list
            # transforming the telemetry data into a dictionary. Then it will be Flask to serialize it into JSON
            for telemetry_data in device_telemetry_data:
                #result_location_list.append(telemetry_data.__dict__)
                result_location_list.append(telemetry_data)

            return result_location_list, 200  # return data and 200 OK code
        else:
            return {'error': "Device Not Found !"}, 404

    def post(self, device_id):
        try:

            # The boolean flag force the parsing of POST data as JSON irrespective of the mimetype
            telemetry_data_dict = request.get_json(force=True)

            # Deserialize the payload into a TelemetryMessge object
            #telemetry_message = TelemetryMessage(**telemetry_json_data)

            # Add the telemetry data to the data manager
            self.data_manager.add_device_telemetry_data(device_id, telemetry_data_dict)

            return Response(status=201)  # return 201 Created

        except JSONDecodeError:
            return {'error': "Invalid JSON ! Check the request"}, 400
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500


