import itertools
import os


def unique_pairs(n):
    numbers = range(n)
    pairs = list(itertools.combinations(numbers, 2))
    return pairs

def levenshtein(s1, s2):
    matrix = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]

    for i in range(len(s1) + 1):
        matrix[i][0] = i
    for j in range(len(s2) + 1):
        matrix[0][j] = j

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            matrix[i][j] = min(matrix[i - 1][j] + 1,      # Удаление
                               matrix[i][j - 1] + 1,      # Вставка
                               matrix[i - 1][j - 1] + cost) # Замена

    return matrix[len(s1)][len(s2)]


class TextFileIterator:
    def __init__(self, directory):
        self.directory = directory
        self.files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.files):
            filename = self.files[self.index]
            print(filename)
            self.index += 1
            file_path = os.path.join(self.directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            raise StopIteration