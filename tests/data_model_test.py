import pandas as pd
import pytest

from pandasdatamodel import exceptions
from pandasdatamodel.data_model import PandasDataModel

from .conftest import DummyDataModel


def test_initiating_data_model_with_one_missing_column_raises_an_error():
    df = pd.DataFrame({"FOO": [1, 2]})
    with pytest.raises(exceptions.MissingColumnError) as excinfo:
        DummyDataModel(df)
    msg = str(excinfo.value)
    expected = """Could not initiate data model because of missing columns:\nBAR"""
    assert msg == expected


def test_initiating_data_model_with_multiple_missing_columns_raises_an_error():
    df = pd.DataFrame({"NOT WHAT YOU EXPECT": [1, 2]})
    with pytest.raises(exceptions.MissingColumnError) as excinfo:
        DummyDataModel(df)
    msg = str(excinfo.value)
    expected = [
        "Could not initiate data model because of missing columns:\nFOO\nBAR",
        "Could not initiate data model because of missing columns:\nBAR\nFOO",
    ]
    assert msg in expected


def test_initiating_data_model_with_empty_data_frame_raises_an_error():
    df = pd.DataFrame({})
    with pytest.raises(exceptions.MissingColumnError) as excinfo:
        DummyDataModel(df)
    msg = str(excinfo.value)
    expected = [
        "Could not initiate data model because of missing columns:\nFOO\nBAR",
        "Could not initiate data model because of missing columns:\nBAR\nFOO",
    ]
    assert msg in expected


def test_initiating_data_model_with_exactly_expected_columns_not_raises_error():
    df = pd.DataFrame({"FOO": [1, 2], "BAR": [3, 4]})
    DummyDataModel(df)
    assert True


def test_initiating_data_model_with_expected_columns_plus_other_not_raises_error():
    df = pd.DataFrame({"FOO": [1, 2], "BAR": [3, 4], "BAZ": [3, 4]})
    DummyDataModel(df)
    assert True


def test_data_model_user_defined_attributes_are_detected(dummy_data_model):
    expected = {"BAR", "FOO"}
    assert dummy_data_model.data_model_columns() == expected
    assert DummyDataModel.data_model_columns() == expected


def test_calling_pandas_dataframe_methods_works_on_data_model(dummy_data_model):
    assert dummy_data_model.shape == dummy_data_model.df.shape
    pd.testing.assert_index_equal(dummy_data_model.columns, dummy_data_model.df.columns)
    pd.testing.assert_series_equal(
        dummy_data_model.loc[:, "FOO"], dummy_data_model.df.loc[:, "FOO"]
    )
