from collections import Counter
from typing import List, Tuple

from find_rhymes import to_blocks, extract_line_phonetic_ending, find_rhyme_scheme_full
from text_example import TEXT_EXAMPLE
from transcribe import TranscriptionData, parse_poetry
from utils import TextFileIterator

vowels = 'уыаоэи'


def count_vowels(input_string: str) -> int:
    count = 0
    for char in input_string:
        if char in vowels:
            count += 1
    return count


def get_kind_by_accent_position(_scheme: List[Tuple[int, int]], block: List[List[TranscriptionData]]) -> str | None:
    kinds_counter = Counter()

    for idx1, idx2 in _scheme:
        line1 = block[idx1]
        ending1 = extract_line_phonetic_ending(line1)
        line2 = block[idx2]
        ending2 = extract_line_phonetic_ending(line2)

        kind = get_kind_by_accent_position_for_2_endings(ending1, ending2)
        if kind:
            kinds_counter[kind] += 1

    if kinds_counter:
        most_common_kinds = kinds_counter.most_common(2)
        if len(most_common_kinds) > 1 and most_common_kinds[0][1] == most_common_kinds[1][1]:
            return None  # Возврат None, если два типа рифмы равны по частоте

        return most_common_kinds[0][0]  # Возврат самого популярного типа рифмы

    return None  # Если нет ни одного вида рифмы


def get_kind_by_accent_position_for_2_endings(ending1: str, ending2: str):
    c1 = count_vowels(ending1)
    c2 = count_vowels(ending2)
    if c1 != c2:
        return None
    if c1 == 1:
        return 'мужская'
    if c1 == 2:
        return 'женская'
    if c1 == 3:
        return 'дактилическая'
    if c1 >= 4:
        return 'гипердактилическая'
    return None


# бессмысленный, т.к. обычно перемежается мужская с женской в каждом четверостишии
def example1():
    lines = parse_poetry(TEXT_EXAMPLE)
    rhyme_scheme_full = find_rhyme_scheme_full(4, lines)
    blocks = to_blocks(4, lines)
    for scheme, block in zip(rhyme_scheme_full, blocks):
        print(get_kind_by_accent_position(scheme.non_perfect, block))


# example1()

def example2():
    lines = parse_poetry(TEXT_EXAMPLE)
    rhyme_scheme_full = find_rhyme_scheme_full(4, lines)
    blocks = to_blocks(4, lines)
    for scheme, block in zip(rhyme_scheme_full, blocks):
        for idx1, idx2 in scheme.non_perfect:
            line1 = block[idx1]
            ending1 = extract_line_phonetic_ending(line1)
            line2 = block[idx2]
            ending2 = extract_line_phonetic_ending(line2)

            kind = get_kind_by_accent_position_for_2_endings(ending1, ending2)
            print(kind)


# example2()

def rate():
    directory_path = 'text-corpora/good'
    text_iterator = TextFileIterator(directory_path)
    counter = Counter()
    for idx, text in enumerate(text_iterator):
        print(idx)
        try:
            lines = parse_poetry(text)
            rhyme_scheme_full = find_rhyme_scheme_full(4, lines)
            blocks = to_blocks(4, lines)
            for scheme, block in zip(rhyme_scheme_full, blocks):
                for idx1, idx2 in scheme.non_perfect:
                    line1 = block[idx1]
                    ending1 = extract_line_phonetic_ending(line1)
                    line2 = block[idx2]
                    ending2 = extract_line_phonetic_ending(line2)

                    kind = get_kind_by_accent_position_for_2_endings(ending1, ending2)
                    counter[kind] += 1

        except:
            pass
    print(counter)

rate()