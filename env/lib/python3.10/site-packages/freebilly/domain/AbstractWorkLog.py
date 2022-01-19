import abc
from typing import Any, Generator, Literal
from freebilly.domain.AbstractWorkSession import AbstractWorkSession
from custom_inherit import DocInheritMeta


class AbstractWorkLog(
    metaclass=DocInheritMeta(style="numpy", abstract_base_class=True)
):
    """
    abstraction for a work log
    """

    __client: str
    __project: str

    @abc.abstractmethod
    def add_session(self, session: AbstractWorkSession) -> None:

        """
        adds an ended work session to this work log.
        Parameters
        ----------
        session : AbstractWorkSession

        Raises
        ------
        ValueError
            if session is not ended.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def total_time(
        self,
        start_time: Any,
        end_time: Any,
        unit: Literal["seconds", "minutes", "hours"] = "hours",
    ) -> float:

        """
        returns the total time spent working between specified moments in the time
        interval spanned by this work log. If no work sessions in the work log match
        the interval requirement, this will return zero, as in 'no time spent working in this
        interval'.

        Parameters
        ----------
        start_time
        end_time
        unit
            the underlying measurement precision is in seconds. If asked a higher unit, rounding at the second decimal place.

        Returns
        -------
        float
        """

        raise NotImplementedError

    @abc.abstractmethod
    def __contains__(self, session: AbstractWorkSession) -> bool:

        """
        Parameters
        ----------
        session : AbstractWorkSession

        Returns
        -------
        bool
            true if this session is contained in this log as per the equality definition.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def get_client(self) -> str:

        """
        Returns
        -------
        str
            this work log's client
        """

        raise NotImplementedError

    @abc.abstractmethod
    def get_project(self) -> str:
        """
        Returns
        -------
        str
            this work log's project
        """

        raise NotImplementedError

    @abc.abstractmethod
    def is_empty(self) -> bool:

        """
        Returns
        -------
        bool
            True if this work log contains no work sessions.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def generate_work_sessions(self) -> Generator[AbstractWorkSession, None, None]:
        """
        Yields
        -------
            AbstractWorkSession
        """

        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self) -> int:
        """
        Returns
        -------
        int
            number of work sessions recorded in this work log
        """
