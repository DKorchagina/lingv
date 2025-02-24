from find_rhymes import find_rhyme_scheme_full
from transcribe import parse_poetry
from utils import TextFileIterator


def rate():
    directory_path = 'text-corpora/bad'
    text_iterator = TextFileIterator(directory_path)  # всего 11_300 файлов
    total_lines = 0
    total_rhymes_found = 0
    for idx, text in enumerate(text_iterator):
        try:
            print(idx)
            rhymes = find_rhyme_scheme_full(10, parse_poetry(text))
            lines_count = text.count('\n') + 1
            rhymes_count = sum([2 * len(scheme.non_perfect) for scheme in rhymes])
            if rhymes_count / lines_count > 0.5:
                with open(f'text-corpora/non-standard-rhyme/{idx}.txt', 'w') as f:
                    f.write(text)
            else:
                with open(f'text-corpora/no-rhyme/{idx}.txt', 'w') as f:
                    f.write(text)
            # print()
            total_lines += lines_count
            total_rhymes_found += rhymes_count
        except:
            print('!')
            pass
    print(f'{100 * total_rhymes_found / total_lines}%')

rate()