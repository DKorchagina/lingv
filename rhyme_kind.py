from dataclasses import dataclass
from typing import List, Tuple

from find_rhymes import find_rhyme_scheme_full
from text_example import TEXT_EXAMPLE
from transcribe import parse_poetry


@dataclass
class RhymeSchemeName:
    scheme: List[Tuple[int, int]]
    name: str


RHYME_SCHEME_NAMES = [
    RhymeSchemeName([(0, 2), (1, 3)], 'Перекрёстная'),
    RhymeSchemeName([(0, 3), (1, 2)], 'Кольцевая'),
    RhymeSchemeName([(0, 1), (2, 3)], 'Парная')
]

def get_rhyme_scheme_name(scheme: List[Tuple[int, int]]):
    t = [s for s in RHYME_SCHEME_NAMES if s.scheme == scheme]
    return None if len(t) == 0 else t[0].name


def example():
    lines = parse_poetry(TEXT_EXAMPLE)
    rhyme_scheme_full = find_rhyme_scheme_full(4, lines)
    for scheme  in rhyme_scheme_full:
        print(f'Для точной: {get_rhyme_scheme_name(scheme.perfect)}')
        print(f'Для неточной: {get_rhyme_scheme_name(scheme.non_perfect)}')

# example()