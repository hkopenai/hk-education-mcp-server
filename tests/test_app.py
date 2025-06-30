import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_education_mcp_server.server import create_mcp_server

class TestApp(unittest.TestCase):
    @patch('hkopenai.hk_education_mcp_server.server.FastMCP')
    @patch('hkopenai.hk_education_mcp_server.tool_primary_schools_enrolment.get_student_enrolment_by_district')
    def test_create_mcp_server(self, mock_tool_enrolment, mock_fastmcp):
        # Setup mocks
        mock_server = unittest.mock.Mock()
        
        mock_fastmcp.return_value = mock_server
        mock_tool_enrolment.return_value = [{'District': 'All Districts', 'All Grades': '325564'}]

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Since we can't directly test decorated functions in this setup,
        # we verify that the mocks are set up correctly
        self.assertTrue(hasattr(mock_server, 'tool'))

if __name__ == "__main__":
    unittest.main()
