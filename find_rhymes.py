import os
from collections import Counter
from dataclasses import dataclass

from text_example import TEXT_EXAMPLE
from transcribe import TranscriptionData, parse_poetry
from typing import List, Tuple

from utils import unique_pairs, levenshtein, TextFileIterator


@dataclass
class RhymeScheme:
    perfect: List[Tuple[int, int]]
    non_perfect: List[Tuple[int, int]]


def find_most_common_rhyme_scheme(schemes: List[RhymeScheme]) -> RhymeScheme:
    perfect_values = [tuple(rhyme.perfect) for rhyme in schemes]
    non_perfect_values = [tuple(rhyme.non_perfect) for rhyme in schemes]

    perfect_counter = Counter(perfect_values)
    most_common_perfect = perfect_counter.most_common(1)
    most_common_perfect_value = most_common_perfect[0][0] if most_common_perfect else []

    non_perfect_counter = Counter(non_perfect_values)
    most_common_non_perfect = non_perfect_counter.most_common(1)
    most_common_non_perfect_value = most_common_non_perfect[0][0] if most_common_non_perfect else []

    return RhymeScheme(perfect=list(most_common_perfect_value),
                       non_perfect=list(most_common_non_perfect_value))


def find_rhyme_scheme(lines: List[List[TranscriptionData]], cycle: int):
    block_rhyme_schemes = find_rhyme_scheme_full(cycle, lines)
    return find_most_common_rhyme_scheme(block_rhyme_schemes)


def find_rhyme_scheme_full(cycle: int, lines: List[List[TranscriptionData]]):
    blocks = to_blocks(cycle, lines)
    check_indexes = unique_pairs(cycle)
    block_rhyme_schemes = [find_rhyme_scheme_for_block(b, check_indexes) for b in blocks]
    return block_rhyme_schemes


def to_blocks(cycle: int, lines: List[List[TranscriptionData]]):
    blocks = [lines[i:i + cycle] for i in range(0, len(lines), cycle)]
    return blocks


def find_rhyme_scheme_for_block(b, check_indexes):
    endings = [extract_line_phonetic_ending(line) for line in b]
    res_perfect = []
    res_non_perfect = []
    check_indexes = [i for i in check_indexes if all(index < len(b) for index in i)]
    for idx_line1, idx_line2 in check_indexes:
        if endings[idx_line1] == endings[idx_line2]:
            res_perfect.append((idx_line1, idx_line2))
        if levenshtein(endings[idx_line1], endings[idx_line2]) * 2 <= min(len(endings[idx_line2]),
                                                                          len(endings[idx_line1])):
            res_non_perfect.append((idx_line1, idx_line2))
    return RhymeScheme(res_perfect, res_non_perfect)


def extract_line_phonetic_ending(line: List[TranscriptionData]):
    res = ""
    for t in line[::-1]:
        if t.stress_index == -1:
            res = t.transcription + res
        else:
            res = t.transcription[t.stress_index:] + res
            return res
    return res


def example():
    print(find_rhyme_scheme_full(4, parse_poetry(TEXT_EXAMPLE)))


# example()

def rate():
    directory_path = 'text-corpora/good'
    text_iterator = TextFileIterator(directory_path)  # всего 11_300 файлов
    total_lines = 0
    total_rhymes_found = 0
    for idx, text in enumerate(text_iterator):
        try:
            print(idx)
            rhymes = find_rhyme_scheme_full(4, parse_poetry(text))
            lines_count = text.count('\n') + 1
            rhymes_count = sum([2 * len(scheme.non_perfect) for scheme in rhymes])

            total_lines += lines_count
            total_rhymes_found += rhymes_count
        except:
            pass
    print(f'{100 * total_rhymes_found / total_lines}%')


# rate()
