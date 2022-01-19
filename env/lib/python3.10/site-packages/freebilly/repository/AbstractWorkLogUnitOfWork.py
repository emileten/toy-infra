from __future__ import annotations
import abc
from custom_inherit import DocInheritMeta
from freebilly.repository.AbstractWorkLogRepository import AbstractWorkLogRepository
from freebilly.domain.AbstractWorkLog import AbstractWorkLog


class AbstractWorkLogUnitOfWork(
    metaclass=DocInheritMeta(style="numpy", abstract_base_class=True)
):
    """
    an interface to access to a repository object and safely commit changes to database
    """

    work_logs: AbstractWorkLogRepository

    def __enter__(self) -> AbstractWorkLogUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self, work_log: AbstractWorkLog) -> None:
        """
        operate a change to the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
