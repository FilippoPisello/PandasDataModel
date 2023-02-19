from dataclasses import MISSING, Field, dataclass

import pandas as pd
import pytest

from pandasdatamodel.custom_field import CustomField
from pandasdatamodel.data_model import PandasDataModel


@dataclass
class DummyDataModel(PandasDataModel):
    FOO: pd.Series = CustomField("FOO")
    BAR: pd.Series = CustomField("BAR")


@pytest.fixture
def dummy_data_model() -> DummyDataModel:
    df = pd.DataFrame({"FOO": [1, 2], "BAR": [3, 4]})
    return DummyDataModel(df)
