from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from deep_translator import GoogleTranslator

tokenizer = AutoTokenizer.from_pretrained("summarizator/")
model = AutoModelForSeq2SeqLM.from_pretrained("summarizator/")
pipe = pipeline("summarization", model=model, tokenizer=tokenizer)


def summarization(text):
    return pipe(text, max_length=300)[0]['summary_text']


def process_history_part1(text):
    strings_to_remove = ["introduction:", "continue the introduction:",
                         "basic situation:", "continue the basic situation:",
                         "character development:", "continued character development:",
                         "building tension:", "continued development of tension:",
                         "plot twist with a fork in the road:"]
    
    title_en, title_index = '', text.lower().find("title:")
    if title_index != -1:
        end_title_index = text.find("\n", title_index)
        title_en = text[title_index + 7:end_title_index].strip()
        text = text[:title_index] + text[end_title_index:]

    title_ru = GoogleTranslator(source='en', target='ru').translate(title_en)

    for string in strings_to_remove:
        start_index = text.lower().find(string.lower())
        end_index = start_index + len(string)
        if start_index != -1:
            text = text[:start_index] + text[end_index:]

    text = text.replace("\n\n", "\n")
    text = text.replace('  ', ' ')

    choices_list = text[text.find("1."):].split("\n")
    choices_en = [choice.strip().replace(f"{i + 1}. ", "") for i, choice in enumerate(choices_list) if choice.strip()]
    choices_ru = [GoogleTranslator(source='en', target='ru').translate(choice) for choice in choices_en]

    text = text[:text.find("1.")]
    text = text.rstrip("\n")
    text = text.lstrip("\n")

    summary = summarization(text)

    result_ru = GoogleTranslator(source='en', target='ru').translate(text)
    paragraphs_ru = [paragraph.strip() for paragraph in result_ru.split("\n") if paragraph.strip()]
    paragraphs_en = [paragraph.strip() for paragraph in text.split("\n") if paragraph.strip()]

    return title_en, title_ru, paragraphs_en, paragraphs_ru, summary, choices_en, choices_ru


def process_history_part2(text):
    strings_to_remove = ["climax:", "the climax:", "continue the climax:", "resolution of the main conflict:",
                         "continue the resolution of the main conflict:", "character unfolding:", "conclusion:"]
    for string in strings_to_remove:
        start_index = text.lower().find(string.lower())
        end_index = start_index + len(string)
        if start_index != -1:
            text = text[:start_index] + text[end_index:]

    text = text.replace("\n\n", "\n")
    text = text.replace('  ', ' ')

    text = text.rstrip("\n")
    text = text.lstrip("\n")

    result_ru = GoogleTranslator(source='en', target='ru').translate(text)

    paragraphs_ru = [paragraph.strip() for paragraph in result_ru.split("\n") if paragraph.strip()]
    paragraphs_en = [paragraph.strip() for paragraph in text.split("\n") if paragraph.strip()]

    return paragraphs_en, paragraphs_ru
