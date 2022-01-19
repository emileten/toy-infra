from tempfile import TemporaryDirectory, NamedTemporaryFile
from pathlib import Path
import pendulum as pdl
from freebilly.repository.CsvWorkLogUnitOfWork import CsvWorkLogUnitOfWork
from freebilly.repository.ConcreteBillUnitOfWork import ConcreteBillUnitOfWork
from freebilly.services.ConcreteServiceLayer import ConcreteServiceLayer
from freebilly.domain.PendulumWorkSession import PendulumWorkSession
from freebilly.domain.OrderedSetWorkLog import OrderedSetWorkLog


def test_start_session():

    with TemporaryDirectory() as fake_dir_path:  # TODO duplications.
        uow = CsvWorkLogUnitOfWork(Path(fake_dir_path))
        work_log, work_session = ConcreteServiceLayer.start_session(
            uow=uow, client="A", project="1"
        )
        assert work_session.get_start_time().diff(pdl.now()).in_minutes() == 0
        assert not work_session.is_ended()
        assert work_log.is_empty()  # because we have no data in this tempdir !


def test_end_session():

    with TemporaryDirectory() as fake_dir_path:  # TODO duplications. See above.
        uow = CsvWorkLogUnitOfWork(Path(fake_dir_path))
        ongoing_session = PendulumWorkSession(start_time=pdl.datetime(1, 1, 1))
        yet_empty_work_log = OrderedSetWorkLog(client="A", project="1")
        ConcreteServiceLayer.end_session(
            uow=uow, work_log=yet_empty_work_log, work_session=ongoing_session
        )
        assert uow.work_logs.exists(client="A", project="1")
        assert uow.work_logs.valid(client="A", project="1")
        assert ongoing_session in uow.work_logs.get(client="A", project="1")


def test_produce_bill():

    # TODO : duplications. See above. Do not rely on your functions in the fakes.
    fake_bill = "Hello. My hourly_rate is $hourly_rate, I worked $quantity hours, so here is the full bill : $total. $cheers."
    expected_output = "Hello. My hourly_rate is 60, I worked 2.0 hours, so here is the full bill : 120.0. Cheers."
    with TemporaryDirectory() as fake_work_log_path:
        uow = CsvWorkLogUnitOfWork(Path(fake_work_log_path))
        work_log = OrderedSetWorkLog(client="A", project="B")
        work_log.add_session(
            PendulumWorkSession(
                start_time=pdl.datetime(1, 1, 1, 1), end_time=pdl.datetime(1, 1, 1, 3)
            )
        )
        work_log.add_session(
            PendulumWorkSession(
                start_time=pdl.datetime(1, 1, 1, 4), end_time=pdl.datetime(1, 1, 1, 7)
            )
        )
        with uow:
            uow.commit(work_log)
        with NamedTemporaryFile() as fake_template_file:
            fake_template_file.write(fake_bill.encode())
            fake_template_file.seek(0)  # rewinding. This is so old school.
            with NamedTemporaryFile() as fake_output_file:
                uow = ConcreteBillUnitOfWork(
                    output_path=Path(fake_output_file.name), overwrite=True
                )
                ConcreteServiceLayer.produce_bill(
                    uow=uow,
                    template_path=Path(fake_template_file.name),
                    work_log_path=Path(fake_work_log_path),
                    client="A",
                    project="B",
                    start_time=pdl.datetime(1, 1, 1, 1),
                    end_time=pdl.datetime(1, 1, 1, 4),
                    hourly_rate=60,
                    extra_info={"cheers": "Cheers"},
                )
                with open(str(uow.output_path)) as actual_output:
                    assert actual_output.read() == expected_output
