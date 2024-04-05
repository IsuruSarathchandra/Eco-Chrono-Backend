from django.test import TestCase
from unittest.mock import patch
from treeDetails.models import TreeSpeciesDetail
from .views import get_tree_details

class TreeDetailsTestCase(TestCase):
    def setUp(self):
        # Create a sample tree species detail for testing
        TreeSpeciesDetail.objects.create(specie_name='Test Tree', specie_growth_factor=1.0)

    @patch('requests.get')
    def test_get_tree_details(self, mock_get):
        # Mocking the response from Wikipedia API
        mock_response = {
            "query": {
                "pages": {
                    "1": {
                        "title": "Test Tree",
                        "extract": "This is a test tree."
                    }
                }
            }
        }
        mock_get.return_value.json.return_value = mock_response

        # Make a request to the view function
        response = self.client.get('/treeDetails/Test%20Tree/100',follow=True)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert the response content
        expected_response = {
            "title": "Test Tree",
            "description": "This is a test tree.",
            "tree age": "31.85"  # Calculated age: circumference / π * growth_factor
        }
        self.assertEqual(response.json(), expected_response)

    @patch('requests.get')
    def test_tree_details_default_growth_factor(self, mock_get):
        # Mocking the response from Wikipedia API
        mock_response = {
            "query": {
                "pages": {
                    "1": {
                        "title": "Unknown Tree",
                        "extract": "This is an unknown tree."
                    }
                }
            }
        }
        mock_get.return_value.json.return_value = mock_response

        # Make a request to the view function for a tree species not in the database
        response = self.client.get('/treeDetails/Unknown%20Tree/100',follow=True)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert the response content when tree species detail not found in the database
        expected_response = {
            "title": "Unknown Tree",
            "description": "This is an unknown tree.",
            "tree age": "31.85"  # Assuming default growth_factor is 1.0
        }
        self.assertEqual(response.json(), expected_response)
