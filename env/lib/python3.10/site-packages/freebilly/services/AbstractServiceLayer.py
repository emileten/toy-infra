import abc
from pathlib import Path
from typing import Tuple
import pendulum as pdl
from custom_inherit import DocInheritMeta
from freebilly.repository.AbstractWorkLogUnitOfWork import AbstractWorkLogUnitOfWork
from freebilly.domain.AbstractWorkLog import AbstractWorkLog
from freebilly.domain.AbstractWorkSession import AbstractWorkSession
from freebilly.repository.AbstractBillUnitOfWork import AbstractBillUnitOfWork


class AbstractServiceLayer(
    metaclass=DocInheritMeta(style="numpy", abstract_base_class=True)
):

    """
    abstraction over use cases of our app.
    """

    @staticmethod
    @abc.abstractmethod
    def start_session(
        uow: AbstractWorkLogUnitOfWork, client: str, project: str
    ) -> Tuple[AbstractWorkLog, AbstractWorkSession]:

        """
        Starts a work session and returns it along with the work log specified,
        from existing data if there is or with a brand new one. associated with the client
        and project specified. The session is not yet added to the log because it's still ongoing, not ended.

        Parameters
        ----------
        uow
        client
        project

        Returns
        -------
        Tuple[AbstractWorkLog, AbstractWorkSession]
            Objects to handle the new session.
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def end_session(
        uow: AbstractWorkLogUnitOfWork,
        work_log: AbstractWorkLog,
        work_session: AbstractWorkSession,
    ) -> None:

        """
        Ends a work session, and commits it to some repository through a unit of work.

        Parameters
        ----------
        uow: AbstractWorkLogUnitOfWork
        work_log: AbstractWorkLog
        work_session: AbstractWorkSession
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
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

        """

        Parameters
        ----------
        uow
        template_path
        work_log_path
        extra_info
        client
        project
        start_time
        end_time
        hourly_rate

        Returns
        -------

        """

        raise NotImplementedError
