# stdlib
import datetime
import random

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus

# this package
import coincidence
from coincidence.utils import generate_falsy_values, generate_truthy_values, with_fixed_datetime


def test_generate_truthy():
	random.seed(1234)

	assert list(generate_truthy_values()) == [
			True,
			"True",
			"true",
			"tRUe",
			'y',
			'Y',
			"YES",
			"yes",
			"Yes",
			"yEs",
			"ON",
			"on",
			'1',
			1,
			]

	assert list(generate_truthy_values(["bar"])) == [
			True,
			"True",
			"true",
			"tRUe",
			'y',
			'Y',
			"YES",
			"yes",
			"Yes",
			"yEs",
			"ON",
			"on",
			'1',
			1,
			"bar",
			]

	assert list(generate_truthy_values(ratio=0.3)) == ['1', "yes", "True", True]


def test_generate_falsy():
	random.seed(1234)

	assert list(generate_falsy_values()) == [
			False,
			"False",
			"false",
			"falSE",
			'n',
			'N',
			"NO",
			"no",
			"nO",
			"OFF",
			"off",
			"oFF",
			'0',
			0,
			]

	assert list(generate_falsy_values(["bar"])) == [
			False,
			"False",
			"false",
			"falSE",
			'n',
			'N',
			"NO",
			"no",
			"nO",
			"OFF",
			"off",
			"oFF",
			'0',
			0,
			"bar",
			]

	assert list(generate_falsy_values(ratio=0.3)) == ['0', "no", "False", False]


@pytest.mark.parametrize(
		"fake_datetime, expected_date",
		[
				pytest.param(datetime.datetime(2020, 10, 13, 2, 20), datetime.datetime(2020, 10, 13), id='0'),
				pytest.param(datetime.datetime(2020, 7, 4, 10, 00), datetime.datetime(2020, 7, 4), id='1'),
				]
		)
def test_with_fixed_datetime(fake_datetime, expected_date: datetime.datetime):

	with with_fixed_datetime(fake_datetime):
		assert datetime.datetime.today() == expected_date
		assert datetime.datetime.now() == fake_datetime

		assert datetime.datetime.__name__ == "datetime"
		assert datetime.datetime.__qualname__ == "datetime"
		assert datetime.datetime.__module__ == "datetime"

		assert datetime.date.today() == expected_date.date()
		assert isinstance(datetime.date.today(), datetime.date)

		assert datetime.date.__name__ == "date"
		assert datetime.date.__qualname__ == "date"
		assert datetime.date.__module__ == "datetime"


def test_is_docker(monkeypatch, tmp_pathplus: PathPlus):
	cgroup = tmp_pathplus / "cgroup"
	monkeypatch.setattr(coincidence.utils, "_cgroup", cgroup)
	monkeypatch.setattr(coincidence.utils, "_dockerenv", (tmp_pathplus / "dockerenv").as_posix())

	assert not cgroup.exists()
	assert not cgroup.is_file()

	assert not coincidence.utils.is_docker()

	(tmp_pathplus / "dockerenv").touch()
	assert coincidence.utils.is_docker()

	(tmp_pathplus / "dockerenv").unlink()
	assert not coincidence.utils.is_docker()

	cgroup.write_text("HelloWorld\n\n\n\ndocker\n\n\nPython\n\n\n")
	assert coincidence.utils.is_docker()

	monkeypatch.setattr(PathPlus, "is_file", lambda *args: True)
	cgroup.unlink()
	assert not coincidence.utils.is_docker()
