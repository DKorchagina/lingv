import re
from ruaccent import RUAccent
from dataclasses import dataclass

@dataclass
class TranscriptionData:
    transcription: str
    stress_index: int

#На данный момент доступно 7 моделей - tiny, tiny2, tiny2.1, turbo2, turbo3, turbo3.1, turbo, big_poetry.
accentizer = RUAccent()
accentizer.load(omograph_model_size='tiny', use_dictionary=True, tiny_mode=False)
print("initialised")


# Словарь для замены гласных с учётом ударений
vowel_not_stressed_transcription = {
    'а': 'а', 'о': 'а', 'у': 'у', 'э': 'э', 'ы': 'ы', 'и': 'и',
    'я': 'а', 'ё': 'о', 'ю': 'у', 'е': 'и',
}

vowel_stressed_transcription = {
    'а': 'а', 'о': 'о', 'у': 'у', 'э': 'э', 'ы': 'ы', 'и': 'и',
    'я': 'а', 'ё': 'о', 'ю': 'у', 'е': 'э',
}

# Словарь для замены согласных с учётом оглушения
consonant_transcription = {
    'б': 'п', 'в': 'ф', 'г': 'к', 'д': 'т', 'ж': 'ш', 'з': 'с',
    'п': 'п', 'ф': 'ф', 'к': 'к', 'т': 'т', 'ш': 'ш', 'с': 'с',
}

# Функция для транскрипции слова с учётом ударений и оглушения
def transcribe_word(word: str, stress_index: int):
    word = word.lower()
    transcribed_word = []
    for i, char in enumerate(word):
        if char in vowel_stressed_transcription:
            # Добавляем ударение, если это ударная гласная
            if i == stress_index:
                transcribed_word.append(vowel_stressed_transcription[char])  # Знак ударения
            else:
                transcribed_word.append(vowel_not_stressed_transcription[char])
        elif char in consonant_transcription:
            # Оглушаем согласные в конце слова или перед глухими согласными
            if i == len(word) - 1 or (i < len(word) - 1 and word[i + 1] in 'цкшщхфпчст'):
                transcribed_word.append(consonant_transcription[char])
            else:
                transcribed_word.append(char)
        else:
            transcribed_word.append(char)
    return ''.join(transcribed_word)

# Функция для транскрипции текста
def transcribe_text(text: str):
    stressed_text = accentizer.process_all(replace_invalid_characters(text))
    words = stressed_text.split()
    transcribed_text = []
    for i, word in enumerate(words):
        stress_index = word.find('+')
        transcribed_word = transcribe_word(word.replace('+',''), stress_index)
        transcribed_text.append(TranscriptionData(transcribed_word, stress_index))
    return transcribed_text

def replace_invalid_characters(text: str):
    # Шаблон для поиска всех символов, которые не являются буквами или цифрами
    pattern = r"[^a-zA-Zа-яА-Я0-9 ]"
    # Замена найденных символов на пустую строку
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def parse_poetry(text: str):
    lines = text.split('\n')
    return [transcribe_text(line) for line in lines]





