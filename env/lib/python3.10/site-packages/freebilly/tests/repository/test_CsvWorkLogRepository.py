import os
import csv
from tempfile import NamedTemporaryFile
from pathlib import Path
import pytest
import pendulum as pdl
from freebilly.repository.CsvWorkLogRepository import CsvWorkLogRepository
from freebilly.domain.AbstractWorkLog import AbstractWorkLog
from freebilly.domain.PendulumWorkSession import PendulumWorkSession

# TODO there is a LOT, LOT of duplicate stuff, consider fixtures, but it's hard because of context managers. Oh. Consider having a util func with a context manager that YIELDS.


def test_manually_written_csv_exists():  # other tests depend on this success
    temp_folder_path = "/tmp"
    with NamedTemporaryFile(dir=temp_folder_path) as temp_fp:
        csv_path = str(Path().joinpath(temp_folder_path, "work_log_A_1.csv"))
        os.rename(temp_fp.name, csv_path)  # because no full name choice option
        with open(csv_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["start_time", "end_time"])
            csv_writer.writerow(
                [pdl.now().to_iso8601_string(), pdl.now().to_iso8601_string()]
            )  # TODO coupling with pendulum
        repo = CsvWorkLogRepository(Path("/tmp"))
        assert repo.exists("A", "1")
        assert not repo.exists("B", "1")
        os.rename(csv_path, temp_fp.name)  # finally, rename back


def test_valid_csv_is_valid():  # TODO this is almost entirely a duplicate of test_exists()
    temp_folder_path = "/tmp"
    with NamedTemporaryFile(dir=temp_folder_path) as temp_fp:
        csv_path = str(Path().joinpath(temp_folder_path, "work_log_A_1.csv"))
        os.rename(temp_fp.name, csv_path)  # because no full name choice option
        with open(csv_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["start_time", "end_time"])
            csv_writer.writerow(
                [pdl.now().to_iso8601_string(), pdl.now().to_iso8601_string()]
            )  # TODO coupling with pendulum
        repo = CsvWorkLogRepository(Path("/tmp"))
        assert repo.valid("A", "1")
        os.rename(csv_path, temp_fp.name)  # finally, rename back


def test_bad_column_csv_is_not_valid():  # TODO this is almost entirely a duplicate of test_valid()
    temp_folder_path = "/tmp"
    with NamedTemporaryFile(dir=temp_folder_path) as temp_fp:
        csv_path = str(Path().joinpath(temp_folder_path, "work_log_A_1.csv"))
        os.rename(temp_fp.name, csv_path)  # because no full name choice option
        with open(csv_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["bad_name", "end_time"])
            csv_writer.writerow(
                [pdl.now().to_iso8601_string(), pdl.now().to_iso8601_string()]
            )  # TODO coupling with pendulum
        repo = CsvWorkLogRepository(Path("/tmp"))
        assert not repo.valid("A", "1")
        os.rename(csv_path, temp_fp.name)  # finally, rename back


def test_empty_csv_is_not_valid():  # TODO this is almost entirely a duplicate of test_valid()
    temp_folder_path = "/tmp"
    with NamedTemporaryFile(dir=temp_folder_path) as temp_fp:
        csv_path = str(Path().joinpath(temp_folder_path, "work_log_A_1.csv"))
        os.rename(temp_fp.name, csv_path)  # because no full name choice option
        with open(csv_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["start_time", "end_time"])
        repo = CsvWorkLogRepository(Path("/tmp"))
        assert not repo.valid("A", "1")
        os.rename(csv_path, temp_fp.name)  # finally, rename back


def test_can_get_log_from_manually_written_csv():
    temp_folder_path = "/tmp"
    my_work_session = PendulumWorkSession(
        start_time=pdl.datetime(1, 1, 1), end_time=pdl.datetime(1, 2, 2)
    )
    with NamedTemporaryFile(dir=temp_folder_path) as temp_fp:
        os.rename(
            temp_fp.name, str(Path().joinpath(temp_folder_path, "work_log_A_1.csv"))
        )  # because no full name choice option
        with open(
            str(Path().joinpath(temp_folder_path, "work_log_A_1.csv")), "w", newline="",
        ) as csv_file:
            my_writer = csv.DictWriter(csv_file, fieldnames=["start_time", "end_time"],)
            my_writer.writeheader()
            my_writer.writerow(
                {
                    "start_time": my_work_session.get_start_time().to_iso8601_string(),
                    "end_time": my_work_session.get_end_time().to_iso8601_string(),
                }
            )

        repo = CsvWorkLogRepository(Path("/tmp"))
        my_work_log = repo.get("A", "1")
        assert isinstance(my_work_log, AbstractWorkLog)
        assert my_work_session in my_work_log
        os.rename(
            str(Path().joinpath(temp_folder_path, "work_log_A_1.csv")), temp_fp.name
        )  # finally, rename back


def test_getting_non_existing_log_from_repo_fails():
    repo = CsvWorkLogRepository(Path("/tmp"))
    with pytest.raises(ValueError):
        repo.get("A", "1")
