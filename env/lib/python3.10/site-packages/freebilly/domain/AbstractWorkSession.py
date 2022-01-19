from __future__ import annotations
from typing import Any
import abc
from custom_inherit import DocInheritMeta


class AbstractWorkSession(
    metaclass=DocInheritMeta(style="numpy", abstract_base_class=True)
):

    """
    abstraction for a work session
    """

    __start_time: Any
    __end_time: Any

    # #TODO Am I supposed to write an abstract __init__ method ? PyCharm tells me 'Parameters not used...'
    # @abc.abstractmethod
    # def __init__(self, start_time: Any, end_time: Any) -> None:
    #
    #     """
    #     Parameters
    #     ----------
    #     start_time: Any
    #         if None, starts the session, otherwise stores the value provided.
    #     end_time: Any
    #         if None, assigns None to __end_time. Otherwise, if start_time is not None, stores the value provided,
    #         but if start_time is None, throws an exception because ending before starting is weird.
    #
    #     Raises
    #     ------
    #     ValueError
    #         if `start_time` is None and `end_time` isn't.
    #     """
    #
    #     raise NotImplementedError

    @abc.abstractmethod
    def start_session(self) -> None:

        """
        starts this session.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def get_start_time(self) -> Any:

        """
        Returns
        -------
        Any
            the start time of this work session
        """

        raise NotImplementedError

    @abc.abstractmethod
    def end_session(self) -> AbstractWorkSession:

        """
        ends this session by adding a field representing the end time and returns itself.
        Raises
        ------
        TypeError
            if this session was already ended
        @TODO this should raise if it attempts to write an end time that's at or before the start time

        Returns
        -------
        AbstractWorkSession
            self
        """

        raise NotImplementedError

    @abc.abstractmethod
    def is_ended(self) -> bool:

        """
        Returns
        -------
        bool
            true if this session is done.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def get_end_time(self) -> Any:

        """
        Returns
        -------
        Any
            the end time of this work session if it's ended, None otherwise.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def overlaps(self, other: AbstractWorkSession) -> bool:

        """
        check whether this session overlaps with another in time. Both have to be
        ended.

        Parameters
        ----------
        other : AbstractWorkSession

        Returns
        -------
        bool
            false if the time interval of `self` is entirely outside of the time interval of `other`.

        Raises
        ------
        TypeError
            if `self` or `other` are not ended.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def total_time(self) -> int:

        """

        Returns
        -------
        int
            if the session is ended, returns total time spent working during this session in seconds.
        Raises
        ------
        TypeError
            if this session is not ended
        """
