from __future__ import annotations
from typing import Any
from custom_inherit import DocInheritMeta

# TODO work in progress, not usable


class AbstractWorkTime(
    metaclass=DocInheritMeta(style="numpy", abstract_base_class=True)
):

    """
    abstraction for the type of time stamp you need to store in a work log.
    """

    __hours: int
    __minutes: int
    __seconds: int

    def __init__(self, time: Any) -> None:

        """
        Parameters
        ----------
        time: Any
            some representation of time that can offer hours, minutes and seconds.
        """

        raise NotImplementedError

    def now(self) -> AbstractWorkTime:

        """
        Returns
        -------
            AbstractWorkTime
                current time
        """

        raise NotImplementedError

    def diff(self, other: AbstractWorkTime) -> int:

        """

        Parameters
        ----------
        other: AbstractWorkTime

        Returns
        -------
            int
                difference between this object's time stamp and `other`'s time stamp.
        """

        raise NotImplementedError

    def __lt__(self, other: AbstractWorkTime) -> bool:

        raise NotImplementedError

    def __gt__(self, other: AbstractWorkTime) -> bool:

        raise NotImplementedError

    def __eq__(self, other: AbstractWorkTime) -> bool:

        raise NotImplementedError
