"""
Module for creating and running the HK OpenAI Education MCP Server.

This module provides functionality to set up and run an MCP server with tools for educational data in Hong Kong.
"""

import argparse
from fastmcp import FastMCP
from hkopenai.hk_education_mcp_server import tool_primary_schools_enrolment
from typing import Dict, List, Annotated, Optional
from pydantic import Field


def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI education Server")

    @mcp.tool(
        description="Student enrolment in primary schools by district and grade in Hong Kong from Education Bureau"
    )
    def get_student_enrolment_by_district() -> List[Dict]:
        return tool_primary_schools_enrolment.get_student_enrolment_by_district()

    return mcp


def main(args):
    """Parse command line arguments and run the MCP server in the specified mode."""
    server = create_mcp_server()

    if args.sse:
        server.run(transport="streamable-http", host=args.host, port=args.port)
        print(f"MCP Server running in SSE mode on port {args.port}, bound to {args.host}")
    else:
        server.run()
        print("MCP Server running in stdio mode")


if __name__ == "__main__":
    main()
