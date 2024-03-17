from openai import OpenAI
import httpx
from httpx_socks import SyncProxyTransport

import db
import utils

API_KEY = "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"
PROXY = "socks5://artem:g1yT7EsvIvIiklu4Fu5c@proxies.ddns.net:5020"
client = OpenAI(
    api_key=API_KEY,
    http_client=httpx.Client(transport=SyncProxyTransport.from_url(PROXY))
)


def create_history_part1(mood, main_character, place):
    messages = [{"role": "system", "content": f"You are the author of {mood}. Your task is to write {mood} stories in "
                                              f"bright and intriguing language. Details of the story: The main "
                                              f"character is {main_character}, the place of action is {place}. Write "
                                              f"a part of the story consisting of the following parts: the title of "
                                              f"the story, the introduction, the main situation, character "
                                              f"development, suspense and plot twist. Then write about each part, "
                                              f"what should be described in it. Each part should be written in 8 "
                                              f"complete meaningful sentences. i.e. you should write like this: "
                                              f"Title: (title) Introduction: (there is an introduction) Continue the "
                                              f"introduction: (there is a continuation of the introduction), "
                                              f"etc. The frame of the story: 0) The title of the story 1) "
                                              f"Introduction: Write 2 paragraphs about the presentation of the "
                                              f"context. 2) Continue the introduction. 3) Basic situation: Write 2 "
                                              f"paragraphs about: 1. Introduction to the world of characters. 2. The "
                                              f"presentation of the main conflict, the unfolding of the plot / "
                                              f"situation, about what underlies the story. 4) Continue the basic "
                                              f"situation. 5) Character development: Write 2 paragraphs about: 1. "
                                              f"Presentation and description of the main character traits of the main "
                                              f"character. 2. The representation of internal and external conflicts "
                                              f"is in character. 6) Continued character development. 7) Raising "
                                              f"tension: Write 2 paragraphs about: 1. Exacerbating the conflict, "
                                              f"creating tension in the plot of the story. 2. The character faces "
                                              f"obstacles. 8) Continue to escalate the tension. 9) Plot twist with a "
                                              f"fork in the road: introduce unexpected elements or events. Divide the "
                                              f"plot into three lines, they should all be different. Write three "
                                              f"points about how the situation can develop further (write each one "
                                              f"from a new line and number them the way I write, i.e. 1. 2. 3.): 1. "
                                              f"The standard version of the plot development, which goes by itself. "
                                              f"2. An option with an unexpected twist, the main character takes on "
                                              f"the most interesting thing. 3. An option with an unexpected twist, "
                                              f"but it goes in a completely different direction, you need to come up "
                                              f"with an alternative plot direction relative to other plot development "
                                              f"options. (No need to write in the reply:  The standard version of the "
                                              f"plot development, which goes on by itself, etc.)"}]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8
    )

    history = completion.choices[0].message.content
    print(history)
    title_en, title_ru, paragraphs_en, paragraphs_ru, summary, choices_en, choices_ru \
        = utils.process_history_part1(history)
    return db.add_history_part1(title_en, title_ru, main_character, mood, place,
                                paragraphs_en, paragraphs_ru, summary, choices_en, choices_ru)


def create_history_part2(id_history, decision):
    mood, main_character, place, previous_part, choice = db.load_history_part1(int(id_history), decision)
    messages = [{"role": "system", "content": f"Continue the previous part of the story (genre - {mood}, main character"
                                              f" {main_character}, place - {place}), which is summarized here "
                                              f"{previous_part} with this continuation result {choice}. Next, act "
                                              f"according to the skeleton (call it exactly as I write, even in the "
                                              f"same register): The climax. The peak of tension, where the character "
                                              f"faces the most difficult test. Continue the climax. Resolution of the "
                                              f"main conflict. Continue to resolve the main conflict. Character "
                                              f"development: The evolution of the character as a result of the passed "
                                              f"tests. Internal growth and change. Conclusion: Resolution of the "
                                              f"remaining subheadings and problems. A satisfactory conclusion to the "
                                              f"story."}]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8
    )

    history = completion.choices[0].message.content
    paragraphs_en, paragraphs_ru = utils.process_history_part2(history)
    db.add_history_part2(int(id_history), paragraphs_en, paragraphs_ru)
