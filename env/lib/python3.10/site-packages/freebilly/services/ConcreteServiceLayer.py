from string import Template
from pathlib import Path
from typing import Tuple
import logging
import pendulum as pdl
from freebilly.repository.AbstractWorkLogUnitOfWork import AbstractWorkLogUnitOfWork
from freebilly.repository.AbstractBillUnitOfWork import AbstractBillUnitOfWork
from freebilly.repository.CsvWorkLogRepository import (
    CsvWorkLogRepository,
)  # TODO coupling
from freebilly.services.AbstractServiceLayer import AbstractServiceLayer
from freebilly.domain.OrderedSetWorkLog import OrderedSetWorkLog  # TODO coupling
from freebilly.domain.PendulumWorkSession import PendulumWorkSession  # TODO coupling

logger = logging.getLogger(__name__)


class ConcreteServiceLayer(AbstractServiceLayer):
    @staticmethod
    def start_session(
        uow: AbstractWorkLogUnitOfWork, client: str, project: str
    ) -> Tuple[OrderedSetWorkLog, PendulumWorkSession]:

        logger.info(f"starting session for client {client} and project {project}...")

        work_session = PendulumWorkSession()
        with uow:
            if uow.work_logs.exists(client, project):
                work_log = uow.work_logs.get(client, project)
            else:
                work_log = OrderedSetWorkLog(client, project)

        logger.info(f"session started")

        return work_log, work_session

    @staticmethod
    def end_session(
        uow: AbstractWorkLogUnitOfWork,
        work_log: OrderedSetWorkLog,
        work_session: PendulumWorkSession,
    ):

        logger.info(f"ending session...")

        with uow:
            work_session.end_session()
            work_log.add_session(work_session)
            uow.commit(work_log)

        logger.info(f"session ended")

    @staticmethod
    def produce_bill(
        uow: AbstractBillUnitOfWork,
        template_path: Path,
        work_log_path: Path,
        extra_info: dict,
        client: str,
        project: str,
        start_time: pdl.DateTime,
        end_time: pdl.DateTime,
        hourly_rate: float,
    ) -> None:

        logging.info(
            f"starting bill production for client {client} and project {project}"
        )

        repo = CsvWorkLogRepository(path=work_log_path)
        if not repo.exists(client, project):
            raise ValueError(
                f"could not find any work log data for client {client} and project {project}..."
            )
        work_log = repo.get(client, project)
        quantity = work_log.total_time(start_time, end_time)
        total = round(
            quantity * hourly_rate, 2
        )  # TODO this is business logic leaking into services. This might mean you actually need a Bill domain object, that's a work log and a rate.
        known_keywords = {
            "hourly_rate": hourly_rate,
            "quantity": quantity,
            "total": total,
        }
        if not all(
            [x not in extra_info.keys() for x in ["hourly_rate", "quantity", "total"]]
        ):
            raise ValueError(
                "'hourly_rate', 'quantity', 'total' are special keywords for which data is to be inferred by the program. They "
                "should not appear as keys in the bill info dictionary."
            )
        all_info = extra_info | known_keywords
        with open(str(template_path)) as template_file:
            template_bill = Template(template_file.read())
            filled_bill = template_bill.substitute(all_info)
        # finally, commit to the data.
        with uow:
            uow.commit(filled_bill)

        logging.info("bill produced")
