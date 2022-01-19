from pathlib import Path
from freebilly.repository.AbstractBillUnitOfWork import AbstractBillUnitOfWork


class ConcreteBillUnitOfWork(AbstractBillUnitOfWork):

    output_path: Path

    def __init__(self, output_path: Path, overwrite: bool = False) -> None:
        if not overwrite and output_path.exists():
            raise ValueError(
                "cannot work on an existing bill. set `overwrite` to True to turn off this behavior."
            )
        self.output_path = output_path

    def commit(self, filled_bill: str) -> None:

        with open(str(self.output_path), "w") as fh:
            fh.write(filled_bill)

    def rollback(self):

        pass
