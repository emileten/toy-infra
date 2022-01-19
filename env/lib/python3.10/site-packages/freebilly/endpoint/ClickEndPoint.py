import logging
from pathlib import Path
from yaml import load, Loader
import pendulum as pdl

# TODO coupling with pendulum
from freebilly.services.ConcreteServiceLayer import ConcreteServiceLayer
from freebilly.repository.CsvWorkLogUnitOfWork import CsvWorkLogUnitOfWork
from freebilly.repository.ConcreteBillUnitOfWork import ConcreteBillUnitOfWork
import logging
import click

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@click.group()
@click.option("--debug/--no-debug", default=False)
def freebilly_cli(debug):
    if debug:
        logging.root.setLevel(logging.DEBUG)


@freebilly_cli.command(help="record a work session in a log")
@click.option(
    "--path",
    required=True,
    help="path to the folder where the work log is stored or is to be stored",
)
@click.option(
    "--client", required=True, help="client with whom you're working",
)
@click.option(
    "--project", required=True, help="project on which you're working",
)
def record_session(path: str, client: str, project: str) -> None:

    uow = CsvWorkLogUnitOfWork(Path(path))
    work_log, work_session = ConcreteServiceLayer.start_session(uow, client, project)
    click.confirm("press enter to end the session...")
    logging.info("ending session and pushing to work log...")
    ConcreteServiceLayer.end_session(uow, work_log, work_session)


@freebilly_cli.command(help="produce a work bill")
@click.option(
    "--template_path",
    required=True,
    help="path to the file containing the template bill",
)
@click.option(
    "--work_log_path",
    required=True,
    help="path to the folder where the work log is stored or is to be stored",
)
@click.option(
    "--extra_info_path",
    required=True,
    help="path to yaml file that can be parsed to a dictionary. \
    They keys will be mapped to the keywords contained in the filed identified by the `template_path` argument.\
    keys without a counterpart keyword are ignored, and an exception is raised if a keyword doesn't have a counterpart key, \
    except for the special cases 'hourly_rate', 'quantity' and 'total' for which data is to be inferred by the program.",
)  # TODO instead, you should be able to pass only a yaml to this function from the CIL
@click.option(
    "--bill_output_path", required=True, help="path where to write the produced bill",
)
@click.option(
    "--client", required=True, help="client with whom you're working",
)
@click.option(
    "--project", required=True, help="project on which you're working",
)
@click.option(
    "--start_time",
    required=True,
    help="start time of the period covered by the bill, in ISO8601 format",
)
@click.option(
    "--end_time",
    required=True,
    help="end time of the period covered by the bill, in ISO8601 format",
)
@click.option(
    "--hourly_rate", required=True, help="hourly rate",
)
def produce_bill(
    template_path: str,
    work_log_path: str,
    extra_info_path: str,
    bill_output_path: str,
    client: str,
    project: str,
    start_time: str,
    end_time: str,
    hourly_rate: str,
) -> None:

    with open(extra_info_path, "r") as stream:
        extra_info_dict = load(stream, Loader)

    uow = ConcreteBillUnitOfWork(Path(bill_output_path))
    ConcreteServiceLayer.produce_bill(
        uow=uow,
        template_path=Path(template_path),
        work_log_path=Path(work_log_path),
        extra_info=extra_info_dict,
        client=client,
        project=project,
        start_time=pdl.parse(start_time),
        end_time=pdl.parse(end_time),
        hourly_rate=float(hourly_rate),
    )
