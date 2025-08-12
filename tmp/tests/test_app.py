'''
Unit tests for the Flask application in tmp/app.py
'''
import unittest
import json
from unittest.mock import patch, MagicMock

# Add the project root to the Python path to allow importing modules like data_model
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tmp.app import app
from data_model import Package # Used for creating mock return objects

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    @patch('tmp.app.SessionMaker')
    def test_get_package_success(self, mock_session_maker):
        mock_session = MagicMock()
        mock_package = Package(
            id=1,
            product_id=100,
            height=10.0,
            width=5.0,
            depth=2.0,
            weight=1.5,
            special_handling_instructions="Fragile"
        )
        mock_session.query.return_value.filter.return_value.first.return_value = mock_package
        mock_session_maker.return_value = mock_session

        response = self.client.get('/packages/100')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['height'], 10.0)
        self.assertEqual(data['special_handling_instructions'], "Fragile")
        mock_session.close.assert_called_once()

    @patch('tmp.app.requests.get')
    @patch('tmp.app.SessionMaker')
    def test_get_package_not_found(self, mock_session_maker, mock_requests_get):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_session_maker.return_value = mock_session

        # Mock the response from get_app_details (called in abort(404))
        mock_response = MagicMock()
        mock_response.json.return_value = {"name": "TestShipper", "version": "0.1"}
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        response = self.client.get('/packages/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The product_id was not found")
        self.assertEqual(data['app_name'], "TestShipper")
        mock_session.close.assert_called_once()
        mock_requests_get.assert_called_once_with('http://localhost:8000/discovery')


    @patch('tmp.app.SessionMaker')
    def test_create_package_success(self, mock_session_maker):
        mock_session = MagicMock()
        
        # Simulate that the commit assigns an ID to the new package
        def mock_commit():
            self.new_package.id = 123
        
        mock_session.commit = MagicMock(side_effect=mock_commit)
        mock_session_maker.return_value = mock_session

        package_data = {
            "product_id": 200,
            "height": 12.0,
            "width": 6.0,
            "depth": 3.0,
            "weight": 2.0,
            "special_handling_instructions": "Handle with care"
        }
        
        # Store the package instance to be able to check its ID later
        def mock_add(package_instance):
            self.new_package = package_instance

        mock_session.add = MagicMock(side_effect=mock_add)

        response = self.client.post('/packages', json=package_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['package_id'], 123)
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        # session.close() is not called in the success path of create_new_package in app.py

    @patch('tmp.app.SessionMaker')
    def test_create_package_missing_data(self, mock_session_maker):
        response = self.client.post('/packages', json=None)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Missing JSON data in request body")
        mock_session_maker.assert_not_called() # Session should not be created

    @patch('tmp.app.SessionMaker')
    def test_create_package_missing_field(self, mock_session_maker):
        package_data = { # Missing product_id
            "height": 12.0,
            "width": 6.0,
            "depth": 3.0,
            "weight": 2.0
        }
        response = self.client.post('/packages', json=package_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertTrue("Missing required field: 'product_id'" in data['message'])
        # In this app.py version, session is not created if KeyError occurs before session = SessionMaker()
        # However, if it occurs after, session might be created but not closed.
        # Based on current app.py, SessionMaker() is called inside the try block.
        # So, if KeyError on data['product_id'], SessionMaker() is not called.
        mock_session_maker.assert_not_called()


    @patch('tmp.app.SessionMaker')
    def test_update_package_success(self, mock_session_maker):
        mock_session = MagicMock()
        mock_package = Package(
            id=1, product_id=100, height=10.0, width=5.0, depth=2.0, weight=1.5
        )
        mock_session.query.return_value.filter.return_value.first.return_value = mock_package
        mock_session_maker.return_value = mock_session

        update_data = {"height": 11.0, "weight": 1.6}
        response = self.client.put('/packages/1', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['height'], 11.0)
        self.assertEqual(data['weight'], 1.6)
        self.assertEqual(mock_package.height, 11.0) # Check if object was updated
        mock_session.commit.assert_called_once()
        # session.close() is not called in the success path of update_existing_package_by_id

    @patch('tmp.app.SessionMaker')
    def test_update_package_not_found(self, mock_session_maker):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_session_maker.return_value = mock_session

        response = self.client.put('/packages/999', json={"height": 10})
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The package_id was not found")
        # session.close() is called in app.py if package is not found, after the query.
        # However, the final session.close() in app.py is unreachable.
        # The mock_session is created, query is called, then first, then the abort happens.
        # The session.close() after abort is not hit.
        # The session.close() at the end of the function is also not hit.
        # So, no close assertion here based on current app.py structure.

    @patch('tmp.app.SessionMaker')
    def test_delete_package_success(self, mock_session_maker):
        mock_session_query = MagicMock() # For the first SessionMaker call
        mock_package = Package(id=1, product_id=100)
        mock_session_query.query.return_value.filter.return_value.first.return_value = mock_package
        
        mock_session_delete = MagicMock() # For the second SessionMaker call

        # Configure SessionMaker to return different mocks for consecutive calls
        mock_session_maker.side_effect = [mock_session_query, mock_session_delete]

        response = self.client.delete('/packages/1')
        self.assertEqual(response.status_code, 204)
        
        mock_session_query.query.assert_called_once_with(Package)
        mock_session_query.close.assert_called_once() # First session is closed

        mock_session_delete.delete.assert_called_with(mock_package)
        mock_session_delete.commit.assert_called_once()
        # Second session is not closed in app.py success path for delete

    @patch('tmp.app.SessionMaker')
    def test_delete_package_not_found(self, mock_session_maker):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_session_maker.return_value = mock_session

        response = self.client.delete('/packages/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The package_id was not found")
        mock_session.close.assert_called_once() # First session is closed if not found

    def test_discovery_endpoint(self):
        response = self.client.get('/discovery')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "shipping")
        self.assertEqual(data['organization'], "acme")

    def test_liveness_endpoint(self):
        response = self.client.get('/liveness')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], "live")

    def test_readiness_endpoint(self):
        response = self.client.get('/readiness')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], "ready")

if __name__ == '__main__':
    unittest.main()
