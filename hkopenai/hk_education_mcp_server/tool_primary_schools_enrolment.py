"""
Module for fetching student enrolment data in Hong Kong primary schools.

This module provides tools to retrieve and process student enrolment data by district and grade from the Education Bureau.
"""

import requests
import csv
from io import StringIO
from typing import List, Dict


def fetch_student_enrolment_data() -> List[Dict]:
    """Fetch student enrolment data from Education Bureau"""
    url = "http://www.edb.gov.hk/attachment/en/about-edb/publications-stat/figures/tab0307_en.csv"
    response = requests.get(url)
    response.raise_for_status()
    # Decode content as UTF-8 since the user specified the encoding
    content = response.content.decode("utf-8")
    # Parse CSV content
    csv_file = StringIO(content)
    csv_reader = csv.DictReader(csv_file)
    data = [row for row in csv_reader]
    return data


def get_student_enrolment_by_district() -> List[Dict]:
    """Get student enrolment in primary schools by district and grade in Hong Kong

    Returns:
        List of dictionaries containing enrolment data by district and grade
    """
    return fetch_student_enrolment_data()
