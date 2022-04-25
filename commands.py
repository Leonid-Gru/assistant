import re
import requests
import pymorphy2
from bs4 import BeautifulSoup
import os
import webbrowser
import time
import random
from playsound import playsound
from gtts import gTTS
import speech_recognition as sr


# запрос информации из Википедии
def wiki(message):
    WIKI = 'https://ru.m.wikipedia.org/wiki/'
    # регулярное выражение забирает слово или выражение, расположенное после предлогов 'о', 'об', 'про'
    wiki_query = re.search(r'[проб]\s(.{,})', message)[1]
    query_nominative = _convert_to_nominative(wiki_query)
    response = requests.get(WIKI + query_nominative)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        block = soup.find('section', class_='mf-section-0')
        try:
            reference = block.find('p').text
            # регулярное выражение убирает из текста то, что в квадратных скобках
            # заменят тире (голосовой помощник не распознает)
            reference = re.sub(r'\[[~!-?\w\s]{1,}\]|[—]', '-', reference)
            webbrowser.open(WIKI + query_nominative)
            say_message(reference)
        except (AttributeError, TypeError):
            google_search(query_nominative)
    else:
        google_search(message)


# выделяем слово в начальной форме
def _convert_to_nominative(wiki_query):
    query_nominative = ''
    morph = pymorphy2.MorphAnalyzer()
    for query in wiki_query.split():
        origin_query = morph.parse(query)[0]
        nominative = origin_query.inflect({'nomn'}).word
        query_nominative += f'{nominative.capitalize()} '
    return query_nominative


# анекдот
def tell_jokes():
    site = 'https://anekdoty.ru/'
    response = requests.get(site)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        block = soup.find('ul', class_='item-list')
        jokes = block.find_all('div', class_='holder-body')
        joke = random.choice(jokes).text
        say_message(joke)
    else:
        say_message('Нет настроения')


# запуск радио
def play_radio():
    site = 'http://humorfm.by/'
    response = requests.get(site)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        block = soup.find('div', class_='bitrate')
        radio = block.find('a', class_='play-action').get('data-stream')
        webbrowser.open(radio)
    else:
        google_search('радио')


# ищем рецепт коктейля
def give_cocktail():
    site = 'https://ru.inshaker.com/cocktails?q='
    say_message('С чем?')
    message = listen_command()
    if ' ' in message:
        query = message.split()[-1]
    else:
        query = message
    morph = pymorphy2.MorphAnalyzer()
    origin_query = morph.parse(query)[0]
    try:
        query_nominative = origin_query.inflect({'nomn'}).word
        webbrowser.open(site + query_nominative)
    except AttributeError:
        webbrowser.open(site + 'коктейль')


# поиск информации в Google
def google_search(message):
    site = 'https://www.google.com/search?q='
    if ' ' in message:
        query = '+'.join(message.split())
    else:
        query = message
    webbrowser.open(site + query)


# слушаем и записываем нашу речь через микрофон
def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите Вашу команду!")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        our_speech = r.recognize_google(audio, language='ru').lower()
        print(our_speech)
    except sr.UnknownValueError:
        our_speech = listen_command()
    return our_speech


# воспроизведение информации
def say_message(message):
    voice = gTTS(message, lang='ru')
    file_voice_name = 'audio_' + str(time.time()) + '_' + str(random.randint(0, 1000)) + '.mp3'
    voice.save(file_voice_name)
    playsound(file_voice_name)
    print(message)
    os.remove(file_voice_name)
