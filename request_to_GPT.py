import openai
from bd import add_history

openai.api_key = "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"


def create_history(set1, set2, set3):
    messages = [{"role": "system", "content": f"Write a fairy tale for children, the reading of which will take from 5 "
                                              f"to 8 minutes. Come up with a title and 20 paragraphs of the story "
                                              f"from 100 to 300 characters, but do not number them. The fairy tale "
                                              f"should have the following characters and elements: the mood of the "
                                              f"fairy tale {set1},the main character {set2}, the place of "
                                              f"action of the fairy tale {set3}. Add an introduction, conflict, "
                                              f"plot development, climax and resolution to the fairy tale. "
                                              f"Add dialogues to the fairy tale. Give simple names to the heroes."}]
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8
    )
    return chat.choices[0].message.content


def translate_history(text):
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f'Выполни художественный перевод сказки на русский язык {text}. '
                                                f'Имена переводи аккуратно, без особых изменений.'}],
        temperature=0.8
    )
    return chat.choices[0].message.content


def translate_title(text_title):
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f'Выполни художественный перевод названия сказки на русский язык '
                                                f'{text_title}. Имена переводи аккуратно, без особых изменений.'}],
        temperature=0.8
    )
    return chat.choices[0].message.content


def history_to_bd(mood, main_character, place):
    history = create_history(mood, main_character, place)
    print(history)
    paragraphs = history.split("\n\n")
    title = paragraphs[0]
    if title[-1] == '.':
        title = title[:-1]
    print(title)
    paragraphs.pop(0)
    result_arr = [translate_title(title), translate_history(paragraphs[:len(paragraphs) // 2]),
                  translate_history(paragraphs[len(paragraphs) // 2:])]
    current_mood = {'love': 'любовном жанре', 'magic': 'волшебном жанре', 'sad': 'в грустном жанре',
                    'happy': 'в радостном жанре', 'adventure': 'в жанре приключений'}
    current_character = {'boy': 'мальчика', 'girl': 'девочку'}
    current_place = {'city': 'в городе', 'space': 'в космосе', 'farm': 'на ферме', 'jungles': 'в джунглях',
                     'future world': 'в мире будущего', 'magic world': 'в волшебном мире', 'kingdom': 'в королевстве',
                     'past world': 'в мире прошлого', 'school': 'в школе', 'magic forest': 'в волшебном лесу',
                     'sea world': 'в морском мире'}
    annotation = (f'Сказка, написанная искусственным интеллектом в {current_mood} про '
                  f'{current_character[main_character]} {current_place[place]}.')
    add_history(mood + main_character + place, annotation, result_arr)

