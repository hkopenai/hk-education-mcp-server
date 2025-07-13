"""
Module for testing student enrolment data tools.

This module contains unit tests for the functionality related to fetching and processing student enrolment data.
"""

import unittest
from unittest.mock import patch, Mock, MagicMock
from hkopenai.hk_education_mcp_server import tool_primary_schools_enrolment


class TestStudentEnrolment(unittest.TestCase):
    """Class for testing student enrolment data retrieval and processing."""
    @patch("requests.get")
    def test_fetch_student_enrolment_data(self, mock_get):
        """Test fetching student enrolment data from the specified URL."""
        # Setup mock response
        mock_response = Mock()
        mock_response.content = b"District,All Grades,P1,P2,P3,P4,P5,P6\nAll Districts,325564,52071,53353,53371,54747,54591,57431\n"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the function
        result = tool_primary_schools_enrolment.fetch_student_enrolment_data()

        # Verify the call
        mock_get.assert_called_once_with(
            "http://www.edb.gov.hk/attachment/en/about-edb/publications-stat/figures/tab0307_en.csv"
        )

        # Verify the result
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["District"], "All Districts")
        self.assertEqual(result[0]["All Grades"], "325564")

    def test_register_tool(self):
        """Test the registration of the get_student_enrolment_by_district tool."""
        mock_mcp = MagicMock()

        # Call the register function
        tool_primary_schools_enrolment.register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Student enrolment in primary schools by district and grade in Hong Kong from Education Bureau"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_student_enrolment_by_district")

        # Call the decorated function and verify it calls _get_student_enrolment_by_district
        with patch(
            "hkopenai.hk_education_mcp_server.tool_primary_schools_enrolment._get_student_enrolment_by_district"
        ) as mock_get_student_enrolment_by_district:
            decorated_function()
            mock_get_student_enrolment_by_district.assert_called_once()


if __name__ == "__main__":
    unittest.main()
