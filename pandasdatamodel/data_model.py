"""Define Data Models, objects to extend pandas dataframe and control columns.

Sub-classes of DataModel are defined to describe the features of a pandas
data frame. They only check that the data frame has the expected columns and
redirect any other call to the data frame itself, so that regular data frame
methods can be called on the Data Model.

The goal is to provide an easy-to-check interface for the tables used within
the script, so that it can be immediately seen what are their fields.
"""
from abc import ABC
from dataclasses import dataclass

import pandas as pd

from pandasdatamodel.exceptions import MissingColumnError


@dataclass
class PandasDataModel(ABC):
    """Class to extend a pandas data frame to allow for data validation.
    The abstract version is to be inherited to define specific models.

    Args:
        df (pd.DataFrame): the data frame whose structure is to be validated.
        columns_map (dict[str, str]): optional, the mapping from old columns
            to data model columns label.

    Raises:
        ValueError: at creation if expected columns are not in df columns.
    """

    df: pd.DataFrame
    columns_map: dict[str, str] | None = None

    def __post_init__(self) -> None:
        """Check columns at object initiation and link attributes to the df."""
        if self.columns_map is not None:
            self.df.rename(columns=self.columns_map, inplace=True)

        missing_columns = self._get_expected_columns_not_in_df()
        if missing_columns:
            raise MissingColumnError(missing_columns)
        self._drop_columns_not_in_data_model()
        self._pair_model_attributes_to_df_columns()
        self._run_validations()

    def _get_expected_columns_not_in_df(self) -> set[str]:
        """Get the set of columns that are expected but not in df."""
        actual_columns = set(self.df.columns)
        expected_columns = self.data_model_columns()
        return expected_columns - actual_columns

    @classmethod
    def data_model_columns(cls) -> set[str]:
        """Return list of user-defined attributes, coinciding with columns."""
        return {attr for attr in dir(cls) if attr.isupper()}

    def _drop_columns_not_in_data_model(self) -> None:
        unwanted_columns = set(self.df.columns) - self.data_model_columns()
        self.df.drop(columns=unwanted_columns, inplace=True)

    def _pair_model_attributes_to_df_columns(self) -> None:
        """Make calls to DataModel attr return the corresponding df column.

        At object creation, the non-initiated fields return the str set as
        default value. After this method executes, calling the attribute is
        equivalent to calling directly the data frame column, allowing for the
        dataframe-like behavior of the object (DataModel.FOO == df.FOO).
        """
        for data_model_column in self.data_model_columns():
            setattr(self, data_model_column, self.df[data_model_column])

    def _run_validations(self) -> None:
        for label, fld in self.__dataclass_fields__.items():
            validation = getattr(fld, "validation", None)
            if validation is None:
                continue
            fld.validation(self.df[label], **fld.validation_parameters)

    def __getattr__(self, attr):
        """Redirect any attribute call to the dataframe object."""
        return getattr(self.df, attr)
