from tempfile import TemporaryDirectory
from pathlib import Path
import pytest
import pendulum as pdl
import ordered_set
from freebilly.domain.OrderedSetWorkLog import OrderedSetWorkLog
from freebilly.domain.PendulumWorkSession import PendulumWorkSession
from freebilly.repository.CsvWorkLogUnitOfWork import CsvWorkLogUnitOfWork


def test_newly_committed_log_exists():
    my_work_session = PendulumWorkSession(
        start_time=pdl.datetime(1, 1, 1), end_time=pdl.datetime(1, 2, 2)
    )
    non_empty_work_log = OrderedSetWorkLog(
        client="A", project="1", sessions=ordered_set.OrderedSet([my_work_session])
    )
    with TemporaryDirectory() as fake_dir_path:
        with CsvWorkLogUnitOfWork(Path(fake_dir_path)) as uow:
            uow.commit(non_empty_work_log)
        assert uow.work_logs.exists(client="A", project="1")


def test_committing_empty_log_fails():
    empty_work_log = OrderedSetWorkLog(client="A", project="1")
    with TemporaryDirectory() as fake_dir_path:
        with CsvWorkLogUnitOfWork(Path(fake_dir_path)) as uow:
            with pytest.raises(ValueError):
                uow.commit(empty_work_log)


def test_can_get_log_committed():
    my_work_session = PendulumWorkSession(
        start_time=pdl.datetime(1, 1, 1), end_time=pdl.datetime(1, 2, 2)
    )
    non_empty_work_log = OrderedSetWorkLog(
        client="A", project="1", sessions=ordered_set.OrderedSet([my_work_session])
    )
    with TemporaryDirectory() as fake_dir_path:
        with CsvWorkLogUnitOfWork(Path(fake_dir_path)) as uow:
            uow.commit(non_empty_work_log)
        assert uow.work_logs.exists("A", "1")
        retrieved_log = uow.work_logs.get("A", "1")
        assert my_work_session in retrieved_log


def test_can_get_csv_path_of_committed_log():
    my_work_session = PendulumWorkSession(
        start_time=pdl.datetime(1, 1, 1), end_time=pdl.datetime(1, 2, 2)
    )
    non_empty_work_log = OrderedSetWorkLog(
        client="A", project="1", sessions=ordered_set.OrderedSet([my_work_session])
    )
    with TemporaryDirectory() as fake_dir_path:
        with CsvWorkLogUnitOfWork(Path(fake_dir_path)) as uow:
            uow.commit(non_empty_work_log)
        assert uow.work_logs.get_csv_file_path("A", "1") == str(
            Path(fake_dir_path).joinpath("work_log_A_1.csv")
        )
