import unittest
from unittest.mock import patch, Mock
import requests
from hkopenai.hk_education_mcp_server import tool_primary_schools_enrolment

class TestStudentEnrolment(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_student_enrolment_data(self, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.content = b'District,All Grades,P1,P2,P3,P4,P5,P6\nAll Districts,325564,52071,53353,53371,54747,54591,57431\n'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the function
        result = tool_primary_schools_enrolment.fetch_student_enrolment_data()

        # Verify the call
        mock_get.assert_called_once_with('http://www.edb.gov.hk/attachment/en/about-edb/publications-stat/figures/tab0307_en.csv')
        
        # Verify the result
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['District'], 'All Districts')
        self.assertEqual(result[0]['All Grades'], '325564')

    def test_get_student_enrolment_by_district(self):
        # This test would ideally mock fetch_student_enrolment_data
        # but for simplicity, we'll just check if it calls the underlying function
        with patch('hkopenai.hk_education_mcp_server.tool_primary_schools_enrolment.fetch_student_enrolment_data') as mock_fetch:
            mock_fetch.return_value = [{'District': 'All Districts', 'All Grades': '325564'}]
            result = tool_primary_schools_enrolment.get_student_enrolment_by_district()
            mock_fetch.assert_called_once()
            self.assertEqual(result, [{'District': 'All Districts', 'All Grades': '325564'}])

if __name__ == "__main__":
    unittest.main()
 