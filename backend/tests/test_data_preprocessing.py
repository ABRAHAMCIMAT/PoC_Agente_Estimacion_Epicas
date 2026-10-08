"""Tests unitarios de utils/data_preprocessing.py (funciones puras, sin modelos)."""
import pandas as pd

from utils.data_preprocessing import JiraDataPreprocessor


class TestExtractSprintDates:
    """extract_sprint_dates parsea el formato de Sprint usado en los exports de JIRA."""

    def setup_method(self):
        self.preprocessor = JiraDataPreprocessor()

    def test_parses_valid_sprint_string(self):
        start, end = self.preprocessor.extract_sprint_dates("Sprint 1, 01-ene a 31-ene")

        assert start == "2025-01-01"
        assert end == "2025-01-31"

    def test_handles_different_months(self):
        start, end = self.preprocessor.extract_sprint_dates("Sprint 7, 05-ago a 18-sep")

        assert start == "2025-08-05"
        assert end == "2025-09-18"

    def test_returns_none_for_missing_value(self):
        start, end = self.preprocessor.extract_sprint_dates(pd.NA)

        assert start is None
        assert end is None

    def test_returns_none_for_unparseable_string(self):
        start, end = self.preprocessor.extract_sprint_dates("texto sin fechas")

        assert start is None
        assert end is None

    def test_is_case_insensitive_on_month_abbreviation(self):
        start, end = self.preprocessor.extract_sprint_dates("Sprint 2, 10-ENE a 20-FEB")

        assert start == "2025-01-10"
        assert end == "2025-02-20"
