"""
Module for creating and running the HK OpenAI Education MCP Server.

This module provides functionality to set up and run an MCP server with tools for educational data in Hong Kong.
"""

from fastmcp import FastMCP
from .tools import primary_schools_enrolment


def server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI education Server")

    primary_schools_enrolment.register(mcp)

    return mcp
