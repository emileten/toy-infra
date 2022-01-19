from freebilly.repository.ConcreteBillUnitOfWork import ConcreteBillUnitOfWork
from tempfile import NamedTemporaryFile
from pathlib import Path


def test_newly_committed_bill_exists_with_content():

    vbl = "very short bill"

    with NamedTemporaryFile() as fh:
        with ConcreteBillUnitOfWork(output_path=Path(fh.name), overwrite=True) as uow:
            uow.commit(vbl)
        assert Path(uow.output_path).exists()
        with open(str(uow.output_path), mode="r") as opened:
            assert opened.read() == "very short bill"
