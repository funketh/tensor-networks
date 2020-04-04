from enum import Enum
from itertools import tee, cycle, chain, repeat, islice

import numpy as np

from tensor_networks.annotations import *


_T1 = TypeVar('_T1')
_T2 = TypeVar('_T2')

ONE_TENSOR = np.array([1])

def get(l: List[_T1], index: int, default: _T2 = None) -> Union[_T1, _T2]:
    return l[index] if index < len(l) and abs(index) <= len(l) else default


def get_last(l: List[_T1], default: _T2 = None) -> Union[_T1, _T2]:
    return get(l, index=-1, default=default)


def get_last_or_one_tensor(l: List[_T1]) -> Union[_T1, Array]:
    return get_last(l, default=ONE_TENSOR)


def identity(x: _T1) -> _T1:
    return x


class Direction(Enum):
    LEFT_TO_RIGHT = 1
    RIGHT_TO_LEFT = -1


def swing_pairwise(seq: Sequence[_T1],
                   start: int = 0,
                   direction: Direction = Direction.LEFT_TO_RIGHT
                   ) -> Iterator[Tuple[_T1, _T1, Direction]]:
    # TODO: documentation
    seq_rev = list(reversed(seq))[1:-1]
    iter1, iter2 = tee(cycle(chain(seq, seq_rev)))
    next(iter2, None)

    directions = cycle(chain(repeat(Direction.LEFT_TO_RIGHT, len(seq) - 1),
                             repeat(Direction.RIGHT_TO_LEFT, len(seq) - 1)))

    if direction == Direction.RIGHT_TO_LEFT:
        start = 2 * (len(seq) - 1) - start

    return islice(zip(iter1, iter2, directions), start, None)
