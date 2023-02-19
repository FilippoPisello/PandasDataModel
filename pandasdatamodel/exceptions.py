"""Collect custom exceptions."""


class MissingColumnError(Exception):
    """Exception raised when df passed to PandasDataModel misses some columns."""

    def __init__(self, missing_columns: set[str]):
        self.message = self._make_error_message(missing_columns)
        super().__init__(self.message)

    @staticmethod
    def _make_error_message(missing_columns: set[str]) -> str:
        msg = "Could not initiate data model because of missing columns:\n"
        cols_string = "\n".join(missing_columns)
        return msg + cols_string
