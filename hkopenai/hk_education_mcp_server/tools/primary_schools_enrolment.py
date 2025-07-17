"""
Module for fetching student enrolment data in Hong Kong primary schools.

This module provides tools to retrieve and process student enrolment data by district and grade from the Education Bureau.
"""

from typing import List, Dict
from hkopenai_common.csv_utils import fetch_csv_from_url


def register(mcp):
    """Registers the primary schools enrolment tool with the FastMCP server."""

    @mcp.tool(
        description="Student enrolment in primary schools by district and grade in Hong Kong from Education Bureau"
    )
    def get_student_enrolment_by_district() -> List[Dict]:
        """Get student enrolment in primary schools by district and grade in Hong Kong

        Returns:
            List of dictionaries containing enrolment data by district and grade
        """
        return _get_student_enrolment_by_district()


def fetch_student_enrolment_data() -> List[Dict] | Dict:
    """Fetch student enrolment data from Education Bureau"""
    url = "http://www.edb.gov.hk/attachment/en/about-edb/publications-stat/figures/tab0307_en.csv"
    data = fetch_csv_from_url(url, encoding="utf-8")
    if "error" in data:
        return {"type": "Error", "error": data["error"]}
    return data


def _get_student_enrolment_by_district() -> List[Dict] | Dict:
    """Get student enrolment in primary schools by district and grade in Hong Kong

    Returns:
        List of dictionaries containing enrolment data by district and grade
    """
    result = fetch_student_enrolment_data()
    if "error" in result:
        return result
    return result
