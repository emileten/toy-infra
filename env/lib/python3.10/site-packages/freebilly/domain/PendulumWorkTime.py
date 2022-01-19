from freebilly.domain.AbstractWorkTime import AbstractWorkTime
import pendulum as pdl


class PendulumWorkTime(AbstractWorkTime):
    def __init__(self, time: pdl.DateTime):

        raise NotImplementedError

    def now(self) -> AbstractWorkTime:

        raise NotImplementedError

    def diff(self, other: AbstractWorkTime) -> int:

        raise NotImplementedError

    def __lt__(self, other: AbstractWorkTime) -> bool:

        raise NotImplementedError

    def __gt__(self, other: AbstractWorkTime) -> bool:

        raise NotImplementedError

    def __eq__(self, other: AbstractWorkTime) -> bool:

        raise NotImplementedError
