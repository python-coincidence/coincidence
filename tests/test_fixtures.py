# stdlib
import datetime

# 3rd party
from domdf_python_tools.paths import PathPlus


def test_tmp_pathplus(tmp_pathplus: PathPlus):
	assert isinstance(tmp_pathplus, PathPlus)
	assert tmp_pathplus.exists()


def test_fixed_datetime(fixed_datetime):
	assert datetime.datetime.today() == datetime.datetime(2020, 10, 13)
	assert datetime.datetime.now() == datetime.datetime(2020, 10, 13, 2, 20)

	assert datetime.datetime.__name__ == "datetime"
	assert datetime.datetime.__qualname__ == "datetime"
	assert datetime.datetime.__module__ == "datetime"

	assert datetime.date.today() == datetime.date(2020, 10, 13)

	assert datetime.date.__name__ == "date"
	assert datetime.date.__qualname__ == "date"
	assert datetime.date.__module__ == "datetime"


def test_path_separator(path_separator: str):
	assert isinstance(path_separator, str)
