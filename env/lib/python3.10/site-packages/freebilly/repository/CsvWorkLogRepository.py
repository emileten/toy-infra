from typing import List
from pathlib import Path
import csv
import logging
from freebilly.repository.AbstractWorkLogRepository import AbstractWorkLogRepository
from freebilly.domain.AbstractWorkLog import AbstractWorkLog
from freebilly.domain.OrderedSetWorkLog import OrderedSetWorkLog
from freebilly.domain.PendulumWorkSession import PendulumWorkSession
import pendulum as pdl  # TODO this is coupled with pendulum so PendulumWorkSession...


class CsvWorkLogRepository(AbstractWorkLogRepository):

    """
    an instance of an AbstractWorkLogRepository where Csvs are used to store work logs in a folder. 
    """

    __repository_path: Path
    __file_name_prefix: str
    __field_names: List

    def __init__(
        self, path: Path, prefix="work_log", field_names=["start_time", "end_time"]
    ) -> None:

        """
        Parameters
        ----------
        path: Path
            Path.exists() should return True
        """
        if not path.exists():
            raise ValueError("nonexistent path")
        self.__repository_path = path
        self.__file_name_prefix = prefix
        self.__field_names = field_names

    def exists(self, client: str, project: str) -> bool:

        return Path(self.get_csv_file_path(client, project)).exists()

    def valid(self, client: str, project: str) -> bool:
        """
        assumes the file is valid. walks through it until the second line included
        checking the first row is the right header and the second had parsable data.
        TODO coupling with pendulum here.

        Parameters
        ----------
        client: str
        project: str

        Returns
        -------
        If there is a failure in the first or second line or if it couldn't reach two lines,
        returns False, True otherwise.
        """
        if not self.exists(client, project):
            raise ValueError(
                "cannot check validity of work log that does not exist in repository"
            )
        i = 0
        is_valid = True
        with open(self.get_csv_file_path(client, project), newline="") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if i == 0:
                    if row != ["start_time", "end_time"]:
                        logging.warning("invalid header in csv work log file")
                        is_valid = False
                elif i == 1:
                    try:
                        (
                            pdl.parse(row[0]),
                            pdl.parse(row[1]),
                        )  # TODO here is a coupling with PendulumWorkSession
                    except Exception:
                        logging.warning(
                            "unable to parse first row after header in csv work log file"
                        )
                        is_valid = False
                else:
                    break
                i = i + 1
        if i < 2:
            is_valid = False
        return is_valid

    def get(self, client: str, project: str) -> AbstractWorkLog:

        csv_file_path = self.get_csv_file_path(client, project)
        if not self.exists(client, project):
            raise ValueError(
                f"file for client {client} and project {project} does not exist"
            )
        if not self.valid(client, project):
            raise ValueError(
                f"representation of work log in file for client {client} and project {project} is not valid"
            )
        new_work_log = OrderedSetWorkLog(
            client, project
        )  # TODO here is a coupling with OrderedSetWorkLog
        with open(csv_file_path, newline="") as csv_file:
            csv_reader = csv.DictReader(
                csv_file, fieldnames=["start_time", "end_time"],
            )
            next(csv_reader)  # skip header
            for row in csv_reader:
                new_work_log.add_session(
                    PendulumWorkSession(  # TODO here is a coupling with PendulumWorkSession
                        pdl.parse(row["start_time"]), pdl.parse(row["end_time"])
                    )
                )

        return new_work_log

    def get_csv_file_path(self, client: str, project: str) -> str:

        """

        Parameters
        ----------
        client: str
        project: str

        Returns
        -------
        str
            full path to csv file containing that work log
        """

        return str(
            self.__repository_path.joinpath(
                self.__file_name_prefix + "_" + client + "_" + project + ".csv"
            )
        )

    def get_field_names(self):

        return self.__field_names
