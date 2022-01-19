from __future__ import annotations
import abc
from pathlib import Path
from custom_inherit import DocInheritMeta

# TODO priority : write tests for a ConcreteBillUnitOfWork
# make a very short fake template with one thing to fill inside, fill it with a fake dict,
# have a TemporaryFile path, pass this along with filled template to the UnitOfWork, try to retrieve
# the object from temporary file path and check it was properly filled with a simple string equality check.


class AbstractBillUnitOfWork(
    metaclass=DocInheritMeta(style="numpy", abstract_base_class=True)
):

    """
    an interface to safely write bills to storage.
    """

    output_path: Path

    def __enter__(self) -> AbstractBillUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self, filled_bill: str) -> None:
        """
        operate a change to the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
