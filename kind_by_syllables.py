import re
from collections import Counter
from dataclasses import dataclass
from typing import List

from transcribe import accentizer
from utils import TextFileIterator


@dataclass
class Foot:
    scheme: list
    name: str


iamb = Foot(scheme=[0, 1], name="ямб")
trochee = Foot(scheme=[1, 0], name="хорей")
dactyl = Foot(scheme=[1, 0, 0], name="дактиль")
amphibrach = Foot(scheme=[0, 1, 0], name="амфибрахий")
anapaest = Foot(scheme=[0, 0, 1], name="анапест")

normal_foots = [iamb, trochee, dactyl, amphibrach, anapaest]

pyrrhic = Foot(scheme=[0, 0], name="пиррихий")
spondee = Foot(scheme=[1, 1], name="спондей")

special_foots_2 = [pyrrhic, spondee]

tribrach = Foot(scheme=[0, 0, 0], name="трибрахий")
bacchius = Foot(scheme=[0, 1, 1], name="бакхий")
antibacchius = Foot(scheme=[1, 1, 0], name="антибакхий")
cretic = Foot(scheme=[1, 0, 1], name="амфимакр")
molossus = Foot(scheme=[1, 1, 1], name="молосс")

special_foots_3 = [tribrach, bacchius, antibacchius, cretic, molossus]

vowels = 'ёуеыаоэяию'


def to_syllables_scheme(string: str) -> List[int]:
    # Заменяем комбинацию гласная + на '1'
    step_one = re.sub(r'\+[' + vowels + ']', '1', string)

    # Заменяем все оставшиеся гласные на '0'
    step_two = re.sub(r'[' + vowels + r']', '0', step_one)

    # удаляем лишнее
    step_three = re.sub(f'[^{vowels}01]', '', step_two)
    return [int(x) for x in step_three]


def get_kind_by_syllables(string: str):
    stressed_text = accentizer.process_all(string).lower()
    syllable_scheme = to_syllables_scheme(stressed_text)
    kinds_counter = Counter()
    for foot in normal_foots:
        foot_size = len(foot.scheme)
        for idx, syllable in enumerate(syllable_scheme):
            if syllable == foot.scheme[idx % foot_size]:
                kinds_counter[foot.name] += 1

    return kinds_counter.most_common(1)


def example():
    print(get_kind_by_syllables("Тучки небесные вечные странники"))
    print(get_kind_by_syllables("Не выходи из комнаты, не совершай ошибку."))


# example()

def rate():
    directory_path = 'text-corpora/good'
    text_iterator = TextFileIterator(directory_path)
    counter_all = Counter()
    for idx, text in enumerate(text_iterator):
        print(idx)
        counter = Counter()
        for line in text.split('\n'):
            try:
                kind = get_kind_by_syllables(line)[0][0]
                counter[kind] += 1
            except:
                print('error')
        counter_all[counter.most_common(1)[0][0]] += 1
    print(counter_all)

rate()