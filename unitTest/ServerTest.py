import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime

class TestNewData(unittest.TestCase):
    def setUp(self):
        self.app = server.test_client()
        self.app.testing = True

        self.data = {
            "deviceId": "12345",
            "payload": [
                {
                    "time": 1623847200000000000,
                    "values": {
                        "longitude": 12.34,
                        "latitude": 56.78,
                        "speed": 90
                    },
                    "name": "accelerometer",
                    "values": {
                        "x": 1.0,
                        "y": 2.0,
                        "z": 3.0
                    }
                },
                {
                    "time": 1623847200000000000,
                    "name": "gyroscope",
                    "values": {
                        "x": 4.0,
                        "y": 5.0,
                        "z": 6.0
                    }
                }
            ]
        }

    @patch('your_module.get_user_id_by_device_id')
    @patch('your_module.verify_active_session')
    @patch('your_module.get_active_session')
    @patch('your_module.create_new_session_by_smartphone')
    @patch('your_module.collection_sensor.insert_one')
    @patch('your_module.collection_session.find_one_and_update')
    def test_new_data(self, mock_find_one_and_update, mock_insert_one, mock_create_new_session, mock_get_active_session, mock_verify_active_session, mock_get_user_id_by_device_id):
        mock_get_user_id_by_device_id.return_value = "user123"
        mock_verify_active_session.return_value = 1
        mock_get_active_session.return_value = (MagicMock(json={"_id": "session123"}), 200)

        response = self.app.post('/data', data=json.dumps(self.data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        mock_insert_one.assert_called()
        mock_find_one_and_update.assert_called()

if __name__ == '__main__':
    unittest.main()
