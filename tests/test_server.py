"""
Module for testing the MCP server creation.

This module contains unit tests for the server creation functionality of the MCP server.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_education_mcp_server.server import create_mcp_server


class TestApp(unittest.TestCase):
    """Class for testing the MCP server application."""
    @patch("hkopenai.hk_education_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_education_mcp_server.server.tool_primary_schools_enrolment")
    def test_create_mcp_server(self, mock_tool_primary_schools_enrolment, mock_fastmcp):
        """Test the creation of the MCP server and tool decoration."""
        # Setup mocks
        mock_server = Mock()

        # Configure mock_server.tool to return a mock that acts as the decorator
        # This mock will then be called with the function to be decorated
        mock_server.tool.return_value = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify that the tool decorator was called for each tool function
        self.assertEqual(mock_server.tool.call_count, 1)

        # Get all decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_server.tool.return_value.call_args_list
        }
        self.assertEqual(len(decorated_funcs), 1)

        # Call each decorated function and verify that the correct underlying function is called

        decorated_funcs["get_student_enrolment_by_district"]()
        mock_tool_primary_schools_enrolment.get_student_enrolment_by_district.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
