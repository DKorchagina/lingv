from typing import List, Tuple

from find_rhymes import to_blocks, extract_line_phonetic_ending, find_rhyme_scheme_full
from text_example import TEXT_EXAMPLE
from transcribe import TranscriptionData, parse_poetry

vowels = 'уыаоэи'


def open_or_closed(_scheme: List[Tuple[int, int]], block: List[List[TranscriptionData]]):
    closed = 0
    opened = 0
    # print(_scheme, block)
    for idx1, idx2 in _scheme:
        line1 = block[idx1]
        ending1 = extract_line_phonetic_ending(line1)
        line2 = block[idx2]
        ending2 = extract_line_phonetic_ending(line2)
        # print(ending1, ending2, ending1[:-1] in vowels, ending1[:-1], ending2[:-1] in vowels, ending2[:-1])
        if ending1[-1] in vowels and ending2[-1] in vowels:
            opened += 1
        if ending1[-1] not in vowels and ending2[-1] not in vowels:
            closed += 1

    if closed > opened:
        return 'закрытая'
    if closed < opened:
        return 'открытая'
    return 'неясно'


def example():
    lines = parse_poetry(TEXT_EXAMPLE)
    rhyme_scheme_full = find_rhyme_scheme_full(4, lines)
    blocks = to_blocks(4, lines)
    for scheme, block in zip(rhyme_scheme_full, blocks):
        print(open_or_closed(scheme.non_perfect, block))

# example()