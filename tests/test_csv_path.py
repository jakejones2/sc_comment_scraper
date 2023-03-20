import pytest
from app.backend import csv_path
from app.backend.paths import MyPaths


def test_create_ind_dir(config1):
    result = csv_path.create_ind_dir(
        config1.url_input.url_list[0],
        config1.filters,
        config1.datetime,
        1
    )
    assert result == f'{MyPaths.csv_path.as_posix()}/{config1.datetime:%Y-%m-%d %H.%M}/headieone, headie-one-martins-sofa[filters = NE, NS].csv'

def test_create_merged_dir(config2):
    result = csv_path.create_merged_dir(
        config2.settings
    )
    assert result == f'{MyPaths.csv_path.as_posix()}/test_config2(1).csv'