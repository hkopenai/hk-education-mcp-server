"""
Module for testing the primary schools enrolment tool functionality.

This module contains unit tests for fetching and processing student enrolment data.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_education_mcp_server.tools.primary_schools_enrolment import (
    _get_student_enrolment_by_district,
    register,
)


class TestPrimarySchoolsEnrolment(unittest.TestCase):
    """
    Test class for verifying primary schools enrolment functionality.

    This class contains test cases to ensure the data fetching and processing
    for student enrolment data work as expected.
    """

    def test_get_student_enrolment_by_district(self):
        """
        Test the retrieval of student enrolment data by district.

        This test verifies that the function correctly fetches and returns data.
        """
        # Mock the CSV data
        mock_csv_data = [
            {"District": "Central and Western", "P1": "1000", "P2": "950"},
            {"District": "Wan Chai", "P1": "800", "P2": "750"},
        ]

        with patch(
            "hkopenai.hk_education_mcp_server.tools.primary_schools_enrolment.fetch_csv_from_url"
        ) as mock_fetch_csv_from_url:
            # Setup mock response for successful data fetching
            mock_fetch_csv_from_url.return_value = mock_csv_data

            # Test successful data retrieval
            result = _get_student_enrolment_by_district()
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["District"], "Central and Western")
            self.assertEqual(result[0]["P1"], "1000")

            # Test error handling when fetch_csv_from_url returns an error
            mock_fetch_csv_from_url.return_value = {"error": "CSV fetch failed"}
            result = _get_student_enrolment_by_district()
            self.assertEqual(result, {"type": "Error", "error": "CSV fetch failed"})

    def test_register_tool(self):
        """
        Test the registration of the get_student_enrolment_by_district tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_student_enrolment_by_district function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

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
            "hkopenai.hk_education_mcp_server.tools.primary_schools_enrolment._get_student_enrolment_by_district"
        ) as mock_get_student_enrolment_by_district:
            decorated_function()
            mock_get_student_enrolment_by_district.assert_called_once()
